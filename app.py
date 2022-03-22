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

# @app.route("/users", methods=["GET", "POST"])
# def index():
#     for i in data:
#         return i["user"]
   
# get a specific users fights + add a new user to your fights array
# if that user is not in the data file already, add them
@app.route("/users/<string:user>/fights", methods=["GET", "POST"])
def handle_fights(user):
    if request.method == "GET":
       return [item for item in data if item.get('user')==user]
    elif request.method == "POST":
        new_fighter = request.json
        this_user_obj = [item for item in data if item.get('user')==user]
        this_user_obj[0]["fights"].append(new_fighter)
        if new_fighter not in [item.get('user') for item in data]:
            data.append({"user": new_fighter, "fights": [user]})
        return f"new fight was created", 201
    

if __name__ == "__main__":
    app.run(debug = True)
