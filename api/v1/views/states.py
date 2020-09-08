#!/usr/bin/python3

from api.v1.views import app_views
from flask import abort
from flask.globals import request
from models import storage
from models.state import State

settings = {
    'strict_slashes': False,
    'methods': ['GET', 'POST', 'DELETE', 'PUT']
}


@app_views.route('/states', **settings)
@app_views.route('/states/<state_id>', **settings)
def states(state_id=None):
    """ Manages return of /states/ pages """

    # Handle '/states/' cases
    if state_id is None:

        if request.method == "POST":
            form = request.get_json()

            if form is None:
                return "Not a JSON", 400

            if form.get('name') is None:
                return "Missing name", 400

            new_state = State(**form)
            new_state.save()

            return new_state.to_dict(), 201

        if request.method == "GET":
            states = storage.all(State).values()
            states = [state.to_dict() for state in states]
            return states

    # Handle '/states/<state_id>' cases

    # get state
    state = storage.get(State, state_id)

    # abort if state doesn't exist
    if state is None:
        abort(404)

    # if "DELETE", delete state, return empty dict
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return {}

    # if "PUT", update state
    if request.method == "PUT":

        form = request.get_json()

        if form is None:
            return "Not a JSON", 400

        for key, value in form.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)

        state.save()

    # return dict representation of state
    # Flask returns exit code 200 by default-- no need to specify it.
    return state.to_dict()
