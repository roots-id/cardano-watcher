from pymongo import MongoClient
import datetime
import os
import urllib.parse
from keri.core import serdering
import mongomock
import sys
class Store():
    def __init__(self):
        if "pytest" in sys.modules:
            self.db = mongomock.MongoClient().watcher
        else:
            try:
                mongo = MongoClient(
                    host= os.environ["DB_URL"] if "DB_URL" in os.environ else 'mongodb://localhost:27017',
                    username=urllib.parse.quote_plus(os.environ["MONGODB_USER"]) if "MONGODB_USER" in os.environ else None,
                    password=urllib.parse.quote_plus(os.environ["MONGODB_PASSWORD"]) if "MONGODB_PASSWORD" in os.environ else None,
                    authSource="admin"
                )
                self.db = mongo.watcher
            except:
                print("Error connecting to the mongo database")
                exit()


    def list_aids(self):
        aids = self.db.aids.find({},{'_id': 0})
        return list(aids)

    def store_aid(self, aid):
        self.db.aids.replace_one({"prefix": aid['prefix']}, aid, upsert=True)

    def remove_aid(self, prefix):
        delete_result = self.db.aids.delete_one({"prefix": prefix})
        if delete_result.deleted_count == 1:
            return True
        else:
            return False

    def get_aid(self, prefix):
        return self.db.aids.find_one({"prefix": prefix},{'_id': 0})

    def list_witnesses(self):
        aids = self.db.wits.find({},{'_id': 0})
        return list(aids)

    def store_witness(self, wit):
        self.db.wits.replace_one({"prefix": wit['prefix']}, wit, upsert=True)

    def remove_witness(self, prefix):
        delete_result = self.db.wits.delete_one({"prefix": prefix})
        if delete_result.deleted_count == 1:
            return True
        else:
            return False

    def store_witness_status(self, prefix, status):
        self.db.wit_pings.insert_one({"prefix": prefix, "status":status, "timestamp": datetime.datetime.now()})

    def store_kel(self, prefix, sn, kel):
        current_kel = self.db.kels.find({"prefix": prefix, 'sn':sn}).sort([('timestamp', -1)]).limit(1)
        try:
            if kel != current_kel[0]['kel']:
                self.db.kels.insert_one({"prefix": prefix, "sn":sn, "kel": kel, "timestamp": datetime.datetime.now()})
                print("KEL updated for aid", prefix, "sn ", sn)
                self.check_new_witnesses(kel)
        except IndexError:
            self.db.kels.insert_one({"prefix": prefix, "sn": sn, "kel": kel, "timestamp": datetime.datetime.now()})
            print("KEL added for aid", prefix, "sn ", sn)
            self.check_new_witnesses(kel)

    def get_kel(self, prefix):
        return list(self.db.kels.find({"prefix": prefix},{'_id': 0}).sort([('timestamp', -1)]))

    def check_new_witnesses(self, msg):
        serder = serdering.SerderKERI(raw=bytearray(msg, encoding='utf8'))
        witnesses = self.list_witnesses()
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
                    self.store_witness(wit)
                    print("New Witness discovered", wit_prefix)

    def generate_stats(self):
        return {
            "aids": self.db.aids.count_documents({}),
            "cardanoAids": self.db.aids.count_documents({"cardano": True}),
            "witnesses": self.db.wits.count_documents({}),
            "keyEventsTotal": self.db.kels.count_documents({}),
            "keyEventsMean": self.db.kels.count_documents({}) / self.db.aids.count_documents({}),
            "witnessesAvailability": self.db.wit_pings.count_documents({"status": 200}) / self.db.wit_pings.count_documents({})
        }

    def get_users(self):
        return list(self.db.users.find({},{'_id': 0}))

    def get_user(self, prefix):
        return self.db.users.find_one({'prefix': prefix},{'_id': 0})


