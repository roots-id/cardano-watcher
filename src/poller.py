"""Witness Poller"""
import threading
import time
from store import list_aids, list_witnesses, store_witness_status
from agent import Agent
import os
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from pycardano import * 
import requests


NETWORK = Network.TESTNET
BLOCKFROST_PROJECT_ID = os.environ['BLOCKFROST_API_KEY']
METADATA_LABEL = int(''.join([str(ord(char) - 96) for char in 'KERIWATCHER'.lower()]))
POLLING_DELAY = 30 # seconds


class Poller(threading.Thread):
    def __init__(self, agent: Agent):
        self.agent = agent
        self.api = BlockFrostApi(
            project_id=BLOCKFROST_PROJECT_ID,
            base_url=ApiUrls.preview.value
        )
        threading.Thread.__init__(self)

    def run(self):
        print("Witness Poller is up")
        while True:
            # AIDs POLLER
            print("Polling AIDs")
            aids = list_aids()
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
            witnesses = list_witnesses()
            for wit in witnesses:
                if wit['oobi'] != 'NA':
                    ping = requests.get(wit['oobi'])
                    store_witness_status(wit['prefix'], ping.status_code)

            time.sleep(POLLING_DELAY)

