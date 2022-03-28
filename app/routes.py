from flask import request, jsonify
from werkzeug import exceptions

from app import app
from app.controllers import users, fights
from db_config import get_collection

# get a list of all current users or adds a new user
@app.route("/users", methods=["GET", "POST"])
def handle_users():
    if request.method == "GET":
        response, code = users.index(request)
        return jsonify(response), code
    elif request.method == "POST":
        response, code = users.create(request)
        return jsonify(response), code

   
# Get a specific user's fights or add a new user to your fights array
# If that user is not in the database already, add them
@app.route("/users/<string:user>/fights", methods=["GET", "POST"])
def handle_fights(user):
    if request.method == "GET":
        response, code = fights.index(request, user)
        return jsonify(response), code
    elif request.method == "POST":
        response, code = fights.create(request, user)
