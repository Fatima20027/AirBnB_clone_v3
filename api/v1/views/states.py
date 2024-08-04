#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects
    """
    state_list = []
    state_obj = storage.all('State')
    for obj in state_obj.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_Id(state_id):
    """
    Retrieves a State object
    """
    fet_obj = storage.get('State', str(state_id))
    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """
    Deletes a State object
    """
    fet_obj = storage.get('State', str(state_id))
    if fet_obj is None:
        abort(404)
    storage.delete(fet_obj)
    storage.save()

    return jsonify({})


@app_views.route("/states/<state_id>", methods=["POST"], strict_slashes=False)
def create_state(state_id):
    """
    Creates a State
    """
    request = request.get_json(silent=True)
    if request is None:
        abort(404, 'Not a JSON')
    if request not in "name":
        abort(400, 'Missing name')

    new_state = State(**request)
    new_state.save()
    res = jsonify(new_state.to_json())
    res.status_code = 201

    return res


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    fet_obj = storage.get('State', str(state_id))
    if fet_obj is None:
        abort(404)
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, 'Not a JSON')

    for key, val in request_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fet_obj, key, val)
    fet_obj.save()
    return jsonify(fet_obj.to_json())
