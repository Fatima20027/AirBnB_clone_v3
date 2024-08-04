#!/usr/bin/python3
"""
Route for handling State objects and operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects.
    """
    state_list = [state.to_json() for state in storage.all('State').values()]
    return jsonify(state_list)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_Id(state_id):
    """
    Retrieves a State object.
    """
    fet_obj = storage.get('State', state_id)
    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def state_delete(state_id):
    """
    Deletes a State object.
    """
    fet_obj = storage.get('State', state_id)
    if fet_obj is None:
        abort(404)
    storage.delete(fet_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a State.
    """
    if not request.is_json:
        abort(400, 'Not a JSON')
    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, 'Missing name')

    new_state = State(**request_data)
    new_state.save()
    res = jsonify(new_state.to_json())
    res.status_code = 201
    return res

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.
    """
    fet_obj = storage.get('State', state_id)
    if fet_obj is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    request_data = request.get_json()
    for key, val in request_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fet_obj, key, val)
    fet_obj.save()
    return jsonify(fet_obj.to_json())
