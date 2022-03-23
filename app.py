from flask import Flask, escape, request, jsonify
from flask_cors import CORS
from werkzeug import exceptions

from db_config import get_collection

app = Flask(__name__)
CORS(app)

# Show all fights
# @app.route("/")
# def index():
#     return jsonify(data) 

# get a list of all current users or adds a new user
@app.route("/users", methods=["GET", "POST"])
def handle_users():
    if request.method == "GET":
        try: 
            collection = get_collection()
            users = collection.find()
            user_list = list(map(lambda user : user["user"],users))
            if not len(user_list):
                raise exceptions.NotFound("No users in the database")
            return jsonify(user_list), 200
        except exceptions.NotFound:
            raise exceptions.NotFound("No users in the database")
        except:
            raise exceptions.InternalServerError()
    elif request.method == "POST":
        new_user = request.json
        try:
        #if new_user["user"] not in [item.get('user') for item in data]:
            collection = get_collection()
            users = collection.find()
            user_list = list(map(lambda user : user["user"],users))
            if new_user["user"] in user_list:
                raise exceptions.BadRequest("User already in database")
            new_user["fights"] = []
            collection.insert_one(new_user)
            # data.append({"user": new_user["user"], "fights": []})
            return f"new user was added", 201
        except exceptions.BadRequest:
            raise exceptions.BadRequest("User already in database")
        except:
            raise exceptions.InternalServerError()

   
# get a specific users fights or add a new user to your fights array
# if that user is not in the data file already, add them
@app.route("/users/<string:user>/fights", methods=["GET", "POST"])
def handle_fights(user):
    if request.method == "GET":
        try: 
            collection = get_collection()
            users = collection.find_one({"user" : user})
            return jsonify(users["fights"]), 200
        except:
            raise exceptions.NotFound("User not found")
        #user_list = list(map(lambda user : user["user"],users))
           #[item for item in data if item.get('user')==user][0]["fights"]
    elif request.method == "POST":
        new_fighter = request.json
        collection = get_collection()
        current_user = collection.find_one({"user": {"$eq": user}})
            
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

