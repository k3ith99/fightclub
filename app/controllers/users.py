from werkzeug import exceptions

from db_config import get_collection

def index(req):
  try: 
    collection = get_collection()
    users = collection.find()
    user_list = list(map(lambda user : user["user"], users))
    if not len(user_list):
        raise exceptions.NotFound("No users in the database")
    return user_list, 200
  except exceptions.NotFound:
    raise exceptions.NotFound("No users in the database")
  except:
    raise exceptions.InternalServerError()

def create(req):
  new_user = req.json
  try:
      collection = get_collection()
      users = collection.find()
      user_list = list(map(lambda user : user["user"],users))
      if new_user["user"] in user_list:
          raise exceptions.BadRequest("User already in database")
      new_user["fights"] = []
      collection.insert_one(new_user)
      return f"new user was added", 201
  except exceptions.BadRequest:
      raise exceptions.BadRequest("User already in database")
  except:
      raise exceptions.InternalServerError()
