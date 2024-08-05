#!/usr/bin/python3
"""
Route for handling Place objects and operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def id_place(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')
    request_data = request.get_json()

    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in request_data:
        abort(400, 'Missing name')

    new_place = Place(**request_data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    request_data = request.get_json()

    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
