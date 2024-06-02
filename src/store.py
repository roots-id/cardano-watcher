from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os
import urllib.parse
from keri.core import serdering


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

def store_witness_status(prefix, status):
    db.wit_pings.insert_one({"prefix": prefix, "status":status, "timestamp": datetime.datetime.now()})

def store_kel(prefix, sn, kel):
    current_kel = db.kels.find({"prefix": prefix, 'sn':sn}).sort([('timestamp', -1)]).limit(1)
    try:
        if kel != current_kel[0]['kel']:
            db.kels.insert_one({"prefix": prefix, "sn":sn, "kel": kel, "timestamp": datetime.datetime.now()})
            print("KEL updated for aid", prefix, "sn ", sn)
            check_new_witnesses(kel)
    except IndexError:
        db.kels.insert_one({"prefix": prefix, "sn": sn, "kel": kel, "timestamp": datetime.datetime.now()})
        print("KEL added for aid", prefix, "sn ", sn)
        check_new_witnesses(kel)

def get_kel(prefix):
    return list(db.kels.find({"prefix": prefix},{'_id': 0}).sort([('timestamp', -1)]))

def check_new_witnesses(msg):
    serder = serdering.SerderKERI(raw=bytearray(msg, encoding='utf8'))
    witnesses = list_witnesses()
    wits = [witnesses['prefix'] for witnesses in witnesses]
    if serder and serder.backs:
        for wit_prefix in serder.backs:
            if wit_prefix not in wits:
                wit = {
                    "prefix": wit_prefix,
                    "alias": wit_prefix,
                    "oobi": "NA",
                    "provider": "NA",
                    "referral": serder.pre
                }
                store_witness(wit)
                print("New Witness discovered", wit_prefix)


