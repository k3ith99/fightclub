from flask import Flask, escape, request, jsonify
from flask_cors import CORS
import json
 
# handle JSON file data
f = open('data.json')
data = json.load(f)

# test
if 'alice' not in [item.get('user') for item in data]:
    print('that user is not in the data')

f.close()


app = Flask(__name__)
CORS(app)

# Show all fights
@app.route("/")
def index():
    return jsonify(data) 

# get a list of all current users or adds a new user
@app.route("/users", methods=["GET", "POST"])
def handle_users():
    if request.method == "GET":
       return jsonify([item.get('user') for item in data])
    elif request.method == "POST":
        new_user = request.json
        if new_user["user"] not in [item.get('user') for item in data]:
            data.append({"user": new_user["user"], "fights": []})
        return f"new user was added", 201
   
# get a specific users fights or add a new user to your fights array
# if that user is not in the data file already, add them
@app.route("/users/<string:user>/fights", methods=["GET", "POST"])
def handle_fights(user):
    if request.method == "GET":
       return jsonify([item for item in data if item.get('user')==user][0]["fights"])
    elif request.method == "POST":
        new_fighter = request.json
        this_user_obj = [item for item in data if item.get('user')==user]
        this_user_obj[0]["fights"].append(new_fighter["new_fighter"])
        if new_fighter["new_fighter"] not in [item.get('user') for item in data]:
            data.append({"user": new_fighter["new_fighter"], "fights": [user]})
        return f"new fight was created", 201
    

if __name__ == "__main__":
    app.run(debug = True)
