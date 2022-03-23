def get_db():
  import pymongo
  from pymongo import MongoClient

  CONN_STRING = "mongodb+srv://noah:noah@cluster0.trdl2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

  client = MongoClient(CONN_STRING)

  return client['fight_club_data']

if __name__ == "__main__":
  import json
  dbname = get_db()
  collection_name = dbname["user_fights"]
  file = open("data.json")
  data = json.load(file)
  collection_name.insert_many(data)
