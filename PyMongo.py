from pymongo import MongoClient


print('********** Connecting to MongoDB. ***********')
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
collection = db["conversations"]
print('********** Connected to MongoDB. ***********')


def insert_into_db(data):
    """
    This is a Python function that inserts data into a MongoDB database and collection, either as a
    single document or multiple documents.

    """
    try:
        if len([data]) > 1:
            collection.insert_many(data)
            return {'status': 1}
        else:
            collection.insert_one(data)
            return {'status': 1}
    except:
        return {'status': 0}














