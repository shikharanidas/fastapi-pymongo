from pymongo import MongoClient
conn=MongoClient("mongodb://localhost:27017/")
db=conn["demo3"]
coll=db["user3"]
