#!/usr/bin/python3
"""
Index route file for the API.
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
     Route that returns the status of the API.
    """
    data = {
        "status": "OK"
    }
    res = jsonify(data)
    res.status_code = 200
    return res
