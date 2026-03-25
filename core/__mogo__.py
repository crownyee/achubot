import motor.motor_asyncio
from core import __json__
jdata = __json__.get_setting_data()
 
uri = jdata['MongoAPI']

class MyMongoDB:
    def __init__(self, uri, database_name, collection_name):
        
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.database = self.mongoConnect[database_name]
        self.collection = self.database[collection_name]
        
my_mongodb = MyMongoDB(uri, 'myproject1', 'collect1')
