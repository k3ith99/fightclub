from werkzeug import exceptions

from db_config import get_collection

def index(req, user):
  try: 
      collection = get_collection()
      users = collection.find_one({"user" : user})
      return users["fights"], 200
  except:
      raise exceptions.NotFound("User not found")
    
def create(req, user):
  new_fighter = req.json
  collection = get_collection()
  current_user = collection.find_one({"user": {"$eq": user}})
      
  current_user["fights"].append(new_fighter["new_fighter"])
  
  print(current_user["fights"])
  collection.update_one(
      {"user": user},
      {"$push": {"fights": new_fighter["new_fighter"]}}
  )
  # Check if user exists in db already; if not, add them
  users = collection.find()
  user_list = list(map(lambda user : user["user"],users))
  if new_fighter["new_fighter"] not in user_list:
      collection.insert_one({"user": new_fighter["new_fighter"], "fights": [user]})
  
  return f"new fight was created", 201
