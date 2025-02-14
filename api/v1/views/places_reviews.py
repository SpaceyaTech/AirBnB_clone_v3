#!/usr/bin/python3

"""Handle  restful API actions for reviews"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews_by_place(place_id):
    """retrieve reviews using place_id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    elif request.method == 'POST':
        new_dict = request.get_json()
        user = storage.get(User, new_dict.get('user_id'))

        if new_dict is None:
            abort(400, 'Not a JSON')
        if new_dict.get("user_id") is None:
            abort(400, 'Missing user_id')
        if new_dict.get("text") is None:
            abort(400, 'Missing text')
        if user is None:
            abort(404)
        review = Review(**new_dict)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_by_review_id(review_id):
    """retrieves review using the review id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        new_dict = request.get_json()
        if new_dict is None:
            abort(400, 'Not a JSON')
        for k, v in new_dict.items():
            setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
