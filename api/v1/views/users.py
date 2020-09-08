#!/usr/bin/python3
""" This is the users api. """

from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.user import User

settings = {
    'strict_slashes': False,
    'methods': ['GET', 'POST', 'DELETE', 'PUT']
}


@app_views.route('/users', **settings)
@app_views.route('/users/<user_id>', **settings)
def users(user_id=None):
    """ Manages return of /users/ pages """

    if user_id is None:
        if request.method == "POST":
            form = request.get_json()
            if form is None:
                return "Not a JSON", 400
            if form.get('email') is None:
                return "Missing email", 400
            if form.get('password') is None:
                return "Missing password", 400
            new_user = User(**form)
            new_user.save()
            return new_user.to_dict(), 201
        if request.method == "GET":
            users = storage.all(User).values()
            users = [user.to_dict() for user in users]
            return jsonify(users)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return {}
    if request.method == "PUT":
        form = request.get_json()
        if form is None:
            return "Not a JSON", 400
        for key, value in form.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
    return user.to_dict()
