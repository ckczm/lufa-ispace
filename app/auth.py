from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app import db
from .models import User

auth = Blueprint('auth', __name__)

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
        return redirect(url_for('auth.login_page'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # check if user already exists in database
    user = User.query.filter_by(email=email).first()

    # if user already exists, redirect back to signup page
    if user:
        flash('User already exists!')
        return redirect(url_for('auth.signup_page'))
    
    # create new user with 0 assets value as a default
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256'))

    # add new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login_page'))

@auth.route('/logout')
@login_required # prevent logout user who isn`t logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))
