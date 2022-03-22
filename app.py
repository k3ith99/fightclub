from flask import Flask, escape, request, jsonify
from flask_cors import CORS

app = Flask(__name__)


@app.route("/users", methods=["GET", "POST"])
def index():
    return "Hello World"


# @app.route("/users/<user>", methods=["GET"])
# def handle_user(user):
    

# @app.route("/users/<user>/fights", methods=["GET", "POST"])
# def handle_fights(user):
    

if __name__ == "__main__":
    app.run(debug = True)
