#!/usr/bin/python3
"""
Initialization file for the api.v1.views package.
"""

from flask import Blueprint

app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *

