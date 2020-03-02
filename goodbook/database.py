import pymongo
from pymongo import MongoClient
import datetime



client = pymongo.MongoClient("mongodb://xinyey2:7861141@cluster0-shard-00-00-2bqe9.mongodb.net:27017,cluster0-shard-00-01-2bqe9.mongodb.net:27017,cluster0-shard-00-02-2bqe9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test_database
collection = db.test_collection
post = {"author": "Mike",
    "text": "My first blog post!",
     "tags": ["mongodb", "python", "pymongo"],
     "date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

