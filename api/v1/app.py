#!/usr/bin/python3
"""
api
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown function that removes the current SQLAlchemy session.
    """
    storage.close()


@app.errorhandler(404)
def nop(error):
    """
    Handle 404 errors by returning a JSON response
    with an error message.
    """
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
