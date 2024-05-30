"""Witness Poller"""
import threading
import time
from store import list_aids
from agent import Agent

class WitnessPoller(threading.Thread):
    def __init__(self, agent):
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
    def __init__(self):
        
        threading.Thread.__init__(self)

    def run(self):
        print("Cardano Poller is up")
        while True:
            print("Cardano polling loop started...")

            time.sleep(70)