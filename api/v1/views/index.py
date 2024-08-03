#!/usr/bin/python3
"""
Index route file for the API.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage 

@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Endpoint that retrieves the number of each objects by type.
    """
    data = {
        "status": "OK"
    }
    res = jsonify(data)
    res.status_code = 200
    return res


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():

    data =  {
        "amenities": storage.count("Amenties"),
        "cities": storage.count("City"), 
        "places": storage.count("Place"), 
        "reviews": storage.count("Review"), 
        "states": storage.count("State"), 
        "users": storage.count("User")
    }
    res = jsonify(data)
    res.status_code = 200
    return res
