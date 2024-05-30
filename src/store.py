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
    db.aids.replace_one({"prefix": aid['prefix']}, aid, upsert=True)

def get_aid(prefix):
    return db.aids.find_one({"prefix": prefix},{'_id': 0})

def list_witnesses():
    aids = db.wits.find({},{'_id': 0})
    return list(aids)

def store_witness(wit):
    db.wits.replace_one({"prefix": wit['prefix']}, wit, upsert=True)

def store_kel(prefix, kel):
    current_kel = db.kels.find({"prefix": prefix}).sort([('timestamp', -1)]).limit(1)
    try:
        if len(kel) != len(current_kel[0]['kel']):
            db.kels.insert_one({"prefix": prefix, "kel": kel, "timestamp": datetime.datetime.now()})
            print("KEL updated for aid ", prefix)
        else:
            print("KEL without changes for ", prefix)
    except IndexError:
        db.kels.insert_one({"prefix": prefix, "kel": kel, "timestamp": datetime.datetime.now()})
        print("KEL added for aid ", prefix)

