"""Witness Poller"""
import threading
import time
from store import list_aids
from agent import Agent
import os
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from pycardano import * 


NETWORK = Network.TESTNET
BLOCKFROST_PROJECT_ID = os.environ['BLOCKFROST_API_KEY']
METADATA_LABEL = int(''.join([str(ord(char) - 96) for char in 'KERIWATCHER'.lower()]))



class WitnessPoller(threading.Thread):
    def __init__(self, agent: Agent):
        self.agent = agent
        threading.Thread.__init__(self)

    def run(self):
        print("Witness Poller is up")
        while True:
            print("Witness polling loop started...")
            aids = list_aids()
            for aid in aids:
                print("Watching", aid['prefix'])
                self.agent.watchAID(prefix=aid['prefix'])
            time.sleep(30)

class CardanoPoller(threading.Thread):
    def __init__(self, agent: Agent):
        self.api = BlockFrostApi(
            project_id=BLOCKFROST_PROJECT_ID,
            base_url=ApiUrls.preview.value
        )
        threading.Thread.__init__(self)

    def run(self):
        print("Cardano Poller is up")
        while True:
            print("Cardano polling loop started...")
            metadatas = self.api.metadata_label_json(METADATA_LABEL)
            for meta in metadatas:
                print(''.join(meta.json_metadata))
            time.sleep(70)