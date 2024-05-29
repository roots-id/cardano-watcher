"""Witness Poller"""
import threading
import time

class WitnessPoller(threading.Thread):
    def __init__(self):
        # self.dbconn = fscmutils.mydbConnection()
        # if self.dbconn is None:
        #     return
        threading.Thread.__init__(self)

    def run(self):
        print("Witness Poller")
        while True:
            # keys = self.redisconn.keys("fscm:messageq:*")
            # for key in keys:
            #     decoded_key = key.decode('utf-8')
            #     data = self.redisconn.get(key)
            #     if data is not None:
            #         d = json.loads(data)
            #         if (int(time.time()*1000) > d['notBefore']):
            #             logging.info(f"Too much wait for key {key.decode('utf-8')}")
            #             # llamar al sender
            #             logging.info(f"dequeueing and sending message {decoded_key}")
            #             fscmsender.MessageSender(json.loads(data.decode('utf-8'))).start()
            #             # borrar el key del queue
            #             self.redisconn.delete(decoded_key)
            time.sleep(5)