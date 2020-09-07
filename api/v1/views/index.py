#!/usr/bin/python3

from api.v1.views import app_views
from flask.json import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status of API """
    return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'])
def counter():
    """ Returns the number of instances for each object type """
    from models import storage
    new_dict = {}
    new_dict.update({"amenities": storage.count("Amenity")})
    new_dict.update({"cities": storage.count("City")})
    new_dict.update({"places": storage.count("Place")})
    new_dict.update({"reviews": storage.count("Review")})
    new_dict.update({"states": storage.count("State")})
    new_dict.update({"users": storage.count("User")})
    return jsonify(new_dict)
