import json
import decimal

from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify
from flask_login import login_required
from flask_login import current_user

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

    return {'all_flights': sorted_flights, 'planets': sorted_planets}

@main.app_template_filter('upper')
def utility_processor(word: str) -> str:
        return word.upper()

@main.app_template_filter('check_status')
def check_status_return_badge_class(flight_status: str) -> str:
    """Method that check current flight status and return proper Bootstrap 
    badge class ('info' for In Progress, 'light' for ' Calculated' flight) 
    for flight status span element."""
    if flight_status == 'In Progress':
        return 'badge-info'
    elif flight_status == 'Not calculated':
        return 'badge-warning'
    elif flight_status == 'Calculated':
        return 'badge-light'

@main.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user)


@main.route('/create_flight', methods=['POST'])
@login_required
def create_flight():
    airline = request.form.get('airline')
    flight_no = request.form.get('flight-no')
    dep = request.form.get('departure')
    dest = request.form.get('destination')
    acft_reg = request.form.get('registration')

    # check if flight is currently in database
    flight = Flight.query.filter_by(flight_no=flight_no).first()

    # if flight already exist, redirect back to main page
    if flight:
        flash('Flight already exists!')
        return redirect(url_for('main.index'))

    # create new flight
    new_flight = Flight(
        airline=airline,
        flight_no=flight_no,
        dep=dep,
        dest=dest,
        acft_reg=acft_reg)
    
    db.session.add(new_flight)
    db.session.commit()

    return redirect(url_for('main.index', user=current_user))

@main.route('/get_flight/<flight_number>', methods=['GET'])
@login_required
def get_flight(flight_number):
    flight = Flight.query.filter_by(flight_no=f'{flight_number}').first()

    if flight is not None:
        flight_data_dict = flight.__dict__
        del flight_data_dict['_sa_instance_state']
        return jsonify(flight_data_dict)
    else:
        return jsonify(None)

@main.route('/delete_flight', methods=['POST'])
@login_required
def delete_flight():
    flight_no = request.form['flight_no'].strip('"')
    flight_to_delete = Flight.query.filter_by(flight_no=f'{flight_no}').first()
    
    db.session.delete(flight_to_delete)
    db.session.commit()

    return redirect(url_for('main.index', user=current_user))

@main.route('/calculate_flight', methods=['POST'])
@login_required
def calculate_flight():
    flight_no = request.form['flight_no'].strip('"')
    etops = json.loads(request.form['etops'])
    fuel_policy = json.loads(request.form['fuel_policy'])

    flight_to_calculate = Flight.query.filter_by(flight_no=f'{flight_no}').first()

    flight_to_calculate.status = 'In Progress'
    db.session.commit()

    # simulate calculating flight by calculating sum of first n elements of 
    # fibonacci sequence in recursion method
    n = 29
    if etops and not fuel_policy:
        n = 32
    elif fuel_policy and not etops:
        n = 34
    elif etops and fuel_policy:
        n = 35
    fibonacci_recursion(n)
    print('Flight successfull calculated.')

    flight_to_calculate.status = 'Calculated'
    db.session.commit()

    return redirect(url_for('main.index', user=current_user))

def fibonacci_recursion(n):
    if n == 0: return 0
    if n == 1: return 1
    
    return fibonacci_recursion(n-2) + fibonacci_recursion(n-1)