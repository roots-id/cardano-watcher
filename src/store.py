from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os
import urllib.parse

mongo = MongoClient(
    # os.environ["DB_URL"],
    host='localhost',
    port=27017,
    username=urllib.parse.quote_plus(os.environ["MONGODB_USER"]) if "MONGODB_USER" in os.environ else None,
    password=urllib.parse.quote_plus(os.environ["MONGODB_PASSWORD"]) if "MONGODB_PASSWORD" in os.environ else None,
    authSource="admin"
)


db = mongo.watcher

def list_aids():
    aids = db.aids.find({},{'_id': 0})
    return list(aids)

def store_aid(aid):
    # TODO resolve OOBI first
    aid['_id'] = aid['prefix']
    db.wits.insert_one(aid)

def list_witnesses():
    aids = db.aids.find({},{'_id': 0})
    return list(aids)

def store_witness(wit):
    # TODO resolve OOBI first
    wit['_id'] = wit['prefix']
    db.wits.insert_one(wit)

