from pymongo import MongoClient

client = MongoClient("mongodb+srv://chue0927:0927@achudatabase0.nlm3xek.mongodb.net/?retryWrites=true&w=majority&appName=achudatabase0")
db = client["myproject1"] 
collection = db["collect1"]  

collection.update_many({}, {"$set": {"money": 0}})