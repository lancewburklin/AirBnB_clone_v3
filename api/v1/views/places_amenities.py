#!/usr/bin/python3
""" This is the amenity api. """

from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv

settings = {
    'strict_slashes': False,
    'methods': ['GET', 'POST', 'DELETE', 'PUT']
}


@app_views.route('/places/<place_id>/amenities', **settings)
@app_views.route('/places/<place_id>/amenities/<amenity_id>', **settings)
def place_amenities(place_id=None, amenity_id=None):
    """ Manages return of /places/amenities/ pages """
    if place_id is None:
        abort(404)
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    storage_type = getenv("HBNB_TYPE_STORAGE")
    if storage_type == "db":
        place_amenities = the_place.amenities
    else:
        place_amenities = the_place.amenity_ids
    if amenity_id is None:
        if request.method == "GET":
            amenities = place_amenities
            amenities = [amenity.to_dict() for amenity in amenities]
            return jsonify(amenities)
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "POST":
        if amenity in place_amenities:
            return amenity.to_dict(), 200
        place_amenities.append(amenity)
        amenity.save()
        return amenity.to_dict(), 201
    if request.method == "DELETE":
        if amenity not in place_amenities:
            abort(404)
        amenity.delete()
        storage.save()
        return {}
