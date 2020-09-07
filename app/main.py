import json
import decimal

from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify
from flask import make_response
from flask import request
from flask_login import login_required
from flask_login import current_user

from functools import wraps

from operator import itemgetter

from app import app
from app import db
from app import models
from .models import User
from .models import Flight
from .models import Planet


main = Blueprint('main', __name__)

@main.context_processor
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

@main.app_template_filter('upper')
def utility_processor(word: str) -> str:
        return word.upper()

@main.app_template_filter('check_status')
def check_status_return_badge_class(flight_status: str) -> str:
    """Method that check current flight status and return proper Bootstrap 
    badge class ('info' for In Progress, 'light' for ' Calculated' flight) 
    for flight status span element."""
    if flight_status == 'In progress':
        return 'badge-info'
    elif flight_status == 'Not calculated':
        return 'badge-warning'
    elif flight_status == 'Calculated':
        return 'badge-light'

@main.route('/index')
@login_required
def index():
    return render_template('index.html')


@main.route('/map')
@login_required
def map():
    return render_template('map.html')


@main.route('/create_flight', methods=['POST'])
def create_flight():
    app.logger.info('Start creating flight')
    if not current_user.is_authenticated:
        return unauthorized_user_response()

    airline = request.form.get('airline')
    flight_no = request.form.get('flight-no')
    dep = request.form.get('departure')
    dest = request.form.get('destination')
    acft_reg = request.form.get('registration')

    flight = Flight.query.filter_by(flight_no=flight_no).first()
    if flight:
        data = {
            'message': f'Flight {flight_no} already exist!',
            'status_code': 409
        }
        response = make_response(data, 409)
        response.headers['Message'] = f'Flight {flight_no} already exist!'
        return response

    # create new flight
    new_flight = Flight(
        airline=airline,
        flight_no=flight_no,
        dep=dep,
        dest=dest,
        acft_reg=acft_reg)
    
    db.session.add(new_flight)
    db.session.commit()

    response = make_response(render_template('index.html'), 201)
    response.headers['Message'] = f'Flight {flight_no} created.'
    return response


@main.route('/get_flight/<flight_number>', methods=['GET'])
def get_flight(flight_number):
    if not current_user.is_authenticated:
        return unauthorized_user_response()

    flight = Flight.query.filter_by(flight_no=f'{flight_number}').first()
    if flight is not None:
        flight_data_dict = flight.__dict__
        del flight_data_dict['_sa_instance_state']
        return jsonify(flight_data_dict)
    else:
        return jsonify(None)


@main.route('/delete_flight', methods=['POST', 'DELETE'])
def delete_flight():
    if not current_user.is_authenticated:
        return unauthorized_user_response()

    flight_no = request.form['flight_no'].strip('"')
    flight_to_delete = Flight.query.filter_by(flight_no=f'{flight_no}').first()

    if not flight_to_delete:
        return no_flight_response(flight_to_delete)
    
    db.session.delete(flight_to_delete)
    db.session.commit()

    return jsonify(None)

@main.route('/calculate_flight', methods=['POST'])
def calculate_flight():
    if not current_user.is_authenticated:
        return unauthorized_user_response()

    flight_no = request.form['flight_no'].strip('"')
    etops = json.loads(request.form['etops'])
    fuel_policy = json.loads(request.form['fuel_policy'])

    flight_to_calculate = Flight.query.filter_by(flight_no=f'{flight_no}').first()

    if not flight_to_calculate:
        return no_flight_response(flight_to_calculate)

    flight_to_calculate.status = 'In Progress'
    db.session.commit()

    # simulate calculating flight by calculating sum of first n elements of 
    # fibonacci sequence in recursion method
    n = 29
    if etops and not fuel_policy:
        n = 31
    elif fuel_policy and not etops:
        n = 32
    elif etops and fuel_policy:
        n = 33
    fibonacci_recursion(n)

    flight_to_calculate.status = 'Calculated'
    db.session.commit()

    response = make_response(render_template('index.html'), 201)
    response.headers['Message'] = f'Flight {flight_no} calculated.'
    return response

def no_flight_response(flight_number: str):
    data = {
        'message': f'Flight {flight_number} doesn`t exist!',
        'status_code': 404
    }
    response = make_response(data, 404)
    response.headers['Message'] = f'Flight {flight_number} doesn`t exist!'
    return response

def unauthorized_user_response():
    data = {'message': f'Unauthorized user!', 'status_code': 401}
    response = make_response(data, 401)
    response.headers['Message'] = f'Unauthorized user!'
    return response

def fibonacci_recursion(n):
    if n == 0: return 0
    if n == 1: return 1
    
    return fibonacci_recursion(n-2) + fibonacci_recursion(n-1)

# @app.after_request
# def redirect_to_index(response):
#     app.logger.info(request.url_rule.endpoint)
#     if request.url_rule.endpoint == 'main.create_flight':
#         app.logger.info('bylem tu?')
#         redirect(url_for('main.index'))
#     return response