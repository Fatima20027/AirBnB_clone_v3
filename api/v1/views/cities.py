#!/usr/bin/python3
"""
Route for handling City objects and operations within a State.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_city(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def id_city(city_id):
    """
     Retrieves a City object.
     """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify(city.to_dict({})), 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_create(state_id):
    """
    Creates a City.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')
    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, 'Missing name')

    request_data['state_id'] = state_id
    new_city = City(**request_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
