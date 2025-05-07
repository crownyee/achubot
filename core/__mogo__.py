import motor.motor_asyncio
import json
with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

uri = jdata['MongoAPI']

class MyMongoDB:
    def __init__(self, uri, database_name, collection_name):
        
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.database = self.mongoConnect[database_name]
        self.collection = self.database[collection_name]
        
my_mongodb = MyMongoDB(uri, 'myproject1', 'collect1')
