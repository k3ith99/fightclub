def get_collection():
  import pymongo
  from pymongo import MongoClient

  CONN_STRING = "mongodb+srv://noah:noah@cluster0.trdl2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

  client = MongoClient(CONN_STRING)

  return client["fight_club_data"]["user_fights"]

if __name__ == "__main__":
  import json
  collection = get_collection()
  file = open("data.json")
  data = json.load(file)
  collection.insert_many(data)

