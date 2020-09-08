#!/usr/bin/python3
""" This is the amenity api. """

from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.amenity import Amenity

settings = {
    'strict_slashes': False,
    'methods': ['GET', 'POST', 'DELETE', 'PUT']
}


@app_views.route('/amenities', **settings)
@app_views.route('/amenities/<amenity_id>', **settings)
def states(state_id=None):
    """ Manages return of /amenities/ pages """

    if amenity_id is None:
        if request.method == "POST":
            form = request.get_json()
            if form is None:
                return "Not a JSON", 400
            if form.get('name') is None:
                return "Missing name", 400
            new_amenity = Amenity(**form)
            new_amenity.save()
            return new_amenity.to_dict(), 201
        if request.method == "GET":
            amenities = storage.all(Amenity).values()
            amenities = [amenity.to_dict() for amenity in amenities]
            return jsonify(amenities)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return {}
    if request.method == "PUT":
        form = request.get_json()
        if form is None:
            return "Not a JSON", 400
        for key, value in form.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
    return amenity.to_dict()
