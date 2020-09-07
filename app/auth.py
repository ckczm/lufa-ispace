from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import make_response
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from operator import itemgetter

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app import db
from .models import User
from .models import Flight
from .models import Planet

auth = Blueprint('auth', __name__)

@auth.context_processor
def inject_variables():
    flights_from_db = Flight.query.all()
    flights_list = [flight.__dict__ for flight in flights_from_db]
    # flights_list is a list of dicts, we want them ordered by id to prevent
    # moving flights on frontend layer i.e. after updating (calculating) flight
    sorted_flights = sorted(flights_list, key=itemgetter('id'))

    planets_from_db = Planet.query.all()
    planets_list = [planet.__dict__ for planet in planets_from_db]
    sorted_planets = sorted(planets_list, key=itemgetter('id'))

    return {'user': current_user, 'all_flights': sorted_flights, 'planets': sorted_planets}

@auth.route('/')
@auth.route('/login')
def login_page():
    return render_template('login.html')

@auth.route('/signup')
def signup_page():
    return render_template('signup.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')

    # check if user actually exists in database
    user = User.query.filter_by(email=email).first()

    # if so, take supplied password, hash it 
    # and compare to hashed password stored in database
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect email or password.')
        response = make_response(render_template('login.html'), 401)
        response.headers['Mmessage'] = 'Incorrect email or password.'
        return response

    login_user(user, remember=remember)

    response = make_response(render_template('index.html'), 200)
    response.headers['Message'] = f'User {user.email} has been logged in.'

    return response

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('User already exists!')
        response = make_response(render_template('signup.html'), 409)
        response.headers['Message'] = 'User already exists!'
        return response
    
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256'))

    # add new user to the database
    db.session.add(new_user)
    db.session.commit()

    response = make_response(render_template('login.html'), 201)
    response.headers['Message'] = f'New user {new_user.email} created!'

    return response

@auth.route('/logout')
@login_required # prevent logout user who isn`t logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))
