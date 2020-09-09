#!/usr/bin/python3
""" Places API """
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.place import Place


# Update api/v1/views/__init__.py to import this new file
setting = {'strict_slashes': False, 'methods':
           ['POST', 'GET', 'DELETE', 'PUT']}


@app_views.route('/cities/<city_id>/places', **setting)
def Places_API(city_id=None):
    """ Get all cities based on State ID """
    if city_id is None:
        abort(404)
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    if request.method == "GET":
        place_list = the_city.places
        place_list = [place.to_dict() for place in place_list]
        return jsonify(place_list)
    if request.method == "POST":
        form = request.get_json()

        if form is None:
            return "Not a JSON", 400
        if form.get('user_id') is None:
            return 'Missing user_id', 400
        if form.get('name') is None:
            return "Missing name", 400

        new_place = Place(**form)
        setattr(new_place, 'city_id', city_id)
        new_place.save()

        return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', **setting)
def full_place(place_id=None):
    """ The other half of the Place API """
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(the_place.to_dict())
    if request.method == "DELETE":
        the_place.delete()
        storage.save()
        return {}
    if request.method == "PUT":
        form = request.get_json()
        if form is None:
            return "Not a JSON", 400
        for key, value in form.items():
            if key not in ['id', 'user_id', 'city_id'
                           'created_at', 'updated_at']:
                setattr(the_place, key, value)
        the_place.save()
        return jsonify(the_place.to_dict())
