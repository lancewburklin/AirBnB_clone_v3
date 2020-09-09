#!/usr/bin/python3
""" City API """
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.state import State


# Update api/v1/views/__init__.py to import this new file
setting = {'strict_slashes': False, 'methods':
           ['POST', 'GET', 'DELETE', 'PUT']}


@app_views.route('/states/<state_id>/cities', **setting)
def cities_API(state_id=None, cities_id=None):
    """ Get all cities based on State ID """
    if state_id is None:
        abort(404)
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    if request.method == "GET":
        city_list = the_state.cities
        city_list = [city.to_dict() for city in city_list]
        return jsonify(city_list)
    if request.method == "POST":
        form = request.get_json()

        if form is None:
            return "Not a JSON", 400

        if form.get('name') is None:
            return "Missing name", 400

        new_city = City(**form)
        setattr(new_city, 'state_id', state_id)
        new_city.save()

        return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', **setting)
def full_city(city_id=None):
    """ The majority of the City API """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(the_city.to_dict())
    if request.method == "DELETE":
        the_city.delete()
        storage.save()
        return {}
    if request.method == "PUT":
        form = request.get_json()
        if form is None:
            return "Not a JSON", 400
        for key, value in form.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(the_city, key, value)
        the_city.save()
        return jsonify(the_city.to_dict())
