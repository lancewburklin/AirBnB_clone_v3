#!/usr/bin/python3
""" review API """
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


setting = {
    'strict_slashes': False,
    'methods': ['POST', 'GET', 'DELETE', 'PUT']
}


@app_views.route('/places/<place_id>/reviews', **setting)
def reviews_API(place_id=None, reviews_id=None):
    """ Get all reviews based on place ID """
    if place_id is None:
        abort(404)
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    if request.method == "GET":
        review_list = the_place.reviews
        review_list = [review.to_dict() for review in review_list]
        return jsonify(review_list)
    if request.method == "POST":
        form = request.get_json()

        if form is None:
            return "Not a JSON", 400

        user_id = form.get('user_id')

        if user_id is None:
            return "Missing user_id", 400

        if storage.get(User, user_id) is None:
            abort(404)

        if form.get('text') is None:
            return "Missing text", 400

        new_review = Review(**form)
        setattr(new_review, 'place_id', place_id)
        new_review.save()

        return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', **setting)
def full_review(review_id=None):
    """ The majority of the review API """
    the_review = storage.get(Review, review_id)
    if the_review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(the_review.to_dict())
    if request.method == "DELETE":
        the_review.delete()
        storage.save()
        return {}
    if request.method == "PUT":
        form = request.get_json()
        if form is None:
            return "Not a JSON", 400
        for key, value in form.items():
            keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            if key not in keys:
                setattr(the_review, key, value)
        the_review.save()
        return jsonify(the_review.to_dict())
