"""Witness Poller"""
import threading
import time
from store import Store
from agent import Agent
import os
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from pycardano import * 
import requests


BLOCKFROST_PROJECT_ID = os.environ['BLOCKFROST_API_KEY']
NETWORK = Network.MAINNET if BLOCKFROST_PROJECT_ID.startswith('mainnet') else Network.TESTNET
METADATA_LABEL = int(''.join([str(ord(char) - 96) for char in 'KERIWATCHER'.lower()]))
POLLING_DELAY = 30 # seconds


class Poller(threading.Thread):
    def __init__(self, agent: Agent, store: Store):
        self.agent = agent
        self.store = store
        self.api = BlockFrostApi(
            project_id=BLOCKFROST_PROJECT_ID,
            base_url= ApiUrls.mainnet.value if BLOCKFROST_PROJECT_ID.startswith('mainnet') else ApiUrls.preview.value

        )
        threading.Thread.__init__(self)

    def run(self):
        print("Witness Poller is up")
        while True:
            # AIDs POLLER
            print("Polling AIDs")
            aids = self.store.list_aids()
            for aid in aids:
                if aid['watched'] and not aid['cardano']:
                    self.agent.resolveOobi(alias=aid['alias'], oobi=aid['oobi'])
            
            # CARDANO POLLER
            print("Crawling Cardano Blockchain")
            page = 1
            while True:
                try:
                    metadatas = self.api.metadata_label_json(METADATA_LABEL, gather_pages=False, count=100, page=page)
                except ApiError:
                    break
                for meta in metadatas:
                    msg = ''.join(meta.json_metadata)
                    self.agent.parseMsg(msg)
                page += 1

            # WITNESS POLLER
            print("Polling Witnesses")
            witnesses = self.store.list_witnesses()
            for wit in witnesses:
                if wit['oobi'] != 'NA':
                    try:
                        ping = requests.get(wit['oobi'])
                        self.store.store_witness_status(wit['prefix'], ping.status_code)
                    except requests.exceptions.ConnectionError:
                        self.store.store_witness_status(wit['prefix'], 404)


            time.sleep(POLLING_DELAY)

