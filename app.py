from flask import Flask, escape, request, jsonify
from flask_cors import CORS
import json

from db_config import get_collection
 
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
        collection = get_collection()
        users = collection.find()
        user_list = list(map(lambda user : user["user"],users))
        return jsonify(user_list)
    elif request.method == "POST":
        new_user = request.json
        #if new_user["user"] not in [item.get('user') for item in data]:
        collection = get_collection()
        users = collection.find()
        user_list = list(map(lambda user : user["user"],users))
        if new_user["user"] not in user_list:
            new_user["fights"] = []
            collection.insert_one(new_user)
            # data.append({"user": new_user["user"], "fights": []})
        return f"new user was added", 201
   
# get a specific users fights or add a new user to your fights array
# if that user is not in the data file already, add them
@app.route("/users/<string:user>/fights", methods=["GET", "POST"])
def handle_fights(user):
    if request.method == "GET":
        collection = get_collection()
        users = collection.find_one({"user" : user})
        print(users)
        #user_list = list(map(lambda user : user["user"],users))

        return jsonify(users["fights"])
           #[item for item in data if item.get('user')==user][0]["fights"]
    elif request.method == "POST":
        new_fighter = request.json
        collection = get_collection()
        current_user = collection.find_one({"user": {"$eq": user}})
        print(current_user)
        #fights = current_user.fights.append(new_fighter["new_fighter"])
        # this_user_obj = [item for item in data if item.get('user')==user]
        # this_user_obj[0]["fights"].append(new_fighter["new_fighter"])
        #if new_fighter["new_fighter"] not in [item.get('user') for item in data]:
            # data.append({"user": new_fighter["new_fighter"], "fights": [user]})
            
        current_user["fights"].append(new_fighter["new_fighter"])
        
        print(current_user["fights"])
        collection.update_one(
            {"user": user},
            {"$push": {"fights": new_fighter["new_fighter"]}},
            upsert = True
            )
        #condition that checks if user exists in db already, if not it adds it
        users = collection.find()
        user_list = list(map(lambda user : user["user"],users))
        if new_fighter["new_fighter"] not in user_list:
            collection.insert_one({"user": new_fighter["new_fighter"], "fights": [user]})

        print("new fight was created")
        
        return f"new fight was created", 201
    

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404

@app.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us"}, 500

if __name__ == "__main__":
    app.run(debug = True)

