from hio import help
from hio.base import doing

from keri.app import directing

import keri.app.oobiing
from keri.app import habbing, configing, oobiing, indirecting, delegating, forwarding, agenting, querying
from keri.app.keeping import Algos
from keri.kering import ConfigurationError
from keri.vdr import credentialing
from keri.app.cli.common import existing, incepting, config
from keri.db import basing
from keri.help import helping
import datetime
from keri.app.cli.common import displaying
from keri.db import dbing
from keri.core.eventing import Siger, Kevery
from keri.core.parsing import Parser
from keri.core import serdering
from keri.kering import sniff, Version
from keri.core.coring import Counter



from store import get_aid, store_kel
import requests



class Agent:
    def __init__(self, name, bran):
        self.bran = bran
        self.name = name

    def initWallet(self):
        kwa = dict()
        kwa["bran"] = self.bran
        hby = habbing.Habery(name=self.name, **kwa)
        rgy = credentialing.Regery(hby=hby, name=self.name)

        print("KERI Keystore created at:", hby.ks.path)
        print("KERI Database created at:", hby.db.path)
        print("KERI Credential Store created at:", rgy.reger.path)
        try:
            hab = hby.makeHab(name=self.name)
        except:
            hab = hby.habByName(self.name)
        print(f'Watcher AID {hab.pre}')
        hby.close()

    def resolveOobi(self, alias, oobi):
        doers = [OobiDoer(name=self.name, oobi=oobi, oobiAlias=alias, bran=self.bran)]
        directing.runController(doers=doers, expire=5.0)
        hby = existing.setupHby(name='watcher', bran=self.bran)
        obr = hby.db.roobi.get(keys=(oobi,))
        if obr:
            res = requests.get(oobi)
            kel = res.text
            store_kel(obr.cid, kel)
            return obr.cid
        else:
            return None
        
    def queryAID(self, prefix):
        # doers = [QueryDoer(name=self.name, alias=self.name,bran=self.bran, pre=prefix)]
        # directing.runController(doers=doers, expire=0.0)
        hby = existing.setupHby(name='watcher', bran=self.bran)
        kever = hby.kevers[prefix]
        ser = kever.serder
        dgkey = dbing.dgKey(ser.preb, ser.saidb)
        wigs = hby.db.getWigs(dgkey)
        dgkey = dbing.dgKey(ser.preb, kever.lastEst.d)
        anchor = hby.db.getAes(dgkey)
        hby.db.getEvt


        # if sn is not None:
        #     said = self.hab.db.getKeLast(key=dbing.snKey(pre=preb,
        #                                                 sn=sn))

        print(kever.state())
        print(kever.serder.ked)

        print("AID", prefix)
        print("Seq No:\t{}".format(kever.sner.num))
        if kever.delegated:
            print("Delegated Identifier")
            print(f"    Delegator:  {kever.delegator} ")
            if anchor:
                print("Anchored")
            else:
                print("Not Anchored")
            print()


        print("\nWitnesses:")
        print("Count:\t\t{}".format(len(kever.wits)))
        print("Receipts:\t{}".format(len(wigs)))
        wigers = [Siger(qb64b=bytes(wig)) for wig in wigs]
        print(wigers[0].qb64b)
        print(wigers[1].qb64b)
        print("Threshold:\t{}".format(kever.toader.num))
        print("\nPublic Keys:\t")
        for idx, verfer in enumerate(kever.verfers):
            print(f'\t{idx+1}. {verfer.qb64}')
        print()
        return 
        
    def watchAID(self, prefix):
        aid = get_aid(prefix)
        if self.resolveOobi(alias=aid['alias'], oobi=aid['oobi']):
            res = requests.get(aid['oobi'])
            kel = res.text
            store_kel(prefix, kel)
            
            # print(kel)
            # ims=bytearray(kel, encoding='utf8')
            # cold = sniff(ims=ims)
            # print(cold)
            # serdery = serdering.Serdery(version=Version)
            # serder = serdery.reap(ims=ims)
            # print(isinstance(serder, serdering.SerderKERI))
            # print(serder.ked)
            # cold = sniff(ims=ims)
            # print(cold)
            # ctr = yield from Parser()._extractor(ims=ims, klas=Counter, cold=cold)
            # print(ctr.code)

            return kel
            


class OobiDoer(doing.DoDoer):
    """ DoDoer for loading oobis and waiting for the results """

    def __init__(self, name, oobi, oobiAlias, bran):

        self.processed = 0
        self.oobi = oobi
        self.hby = existing.setupHby(name=name, bran=bran)
        self.hbyDoer = habbing.HaberyDoer(habery=self.hby)

        obr = basing.OobiRecord(date=helping.nowIso8601())
        if oobiAlias is not None:
            obr.oobialias = oobiAlias

        self.hby.db.oobis.put(keys=(oobi,), val=obr)

        self.obi = keri.app.oobiing.Oobiery(hby=self.hby)
        self.authn = oobiing.Authenticator(hby=self.hby)
        doers = [self.hbyDoer, doing.doify(self.waitDo)]

        super(OobiDoer, self).__init__(doers=doers)

    def waitDo(self, tymth, tock=0.0):
        """ Waits for oobis to load

        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value

        Returns:  doifiable Doist compatible generator method for loading oobis using
        the Oobiery
        """
        # enter context
        self.wind(tymth)
        self.tock = tock
        _ = (yield self.tock)

        # remove previous record of OOBI resolution (--force)
        self.hby.db.roobi.rem(keys=(self.oobi,))

        self.extend(self.obi.doers)
        self.extend(self.authn.doers)

        while not self.obi.hby.db.roobi.get(keys=(self.oobi,)):
            yield 0.25

        self.remove([self.hbyDoer, *self.obi.doers, *self.authn.doers]) 

class QueryDoer(doing.DoDoer):

    def __init__(self, name, alias, bran, pre, **kwa):
        doers = []
        self.hby = existing.setupHby(name=name, bran=bran)
        self.hbyDoer = habbing.HaberyDoer(habery=self.hby)  # setup doer
        hab = self.hby.habByName(alias)

        self.hab = hab

        self.pre = pre
        # self.anchor = anchor

        self.mbd = indirecting.MailboxDirector(hby=self.hby, topics=["/replay", "/receipt", "/reply","/ksn"])
        doers.extend([self.hbyDoer, self.mbd])

        self.toRemove = list(doers)
        doers.extend([doing.doify(self.queryDo)])
        super(QueryDoer, self).__init__(doers=doers, **kwa)

    def queryDo(self, tymth, tock=0.0, **opts):
        """
        Returns:  doifiable Doist compatible generator method
        Usage:
            add result of doify on this method to doers list
        """
        # enter context
        self.wind(tymth)
        self.tock = tock
        _ = (yield self.tock)

        end = helping.nowUTC() + datetime.timedelta(seconds=5)

        print("Querying for updates for", self.pre)
        doer = querying.QueryDoer(hby=self.hby, hab=self.hab, pre=self.pre, kvy=self.mbd.kvy)

        self.extend([doer])

        while helping.nowUTC() < end:
            if doer.done:
                break
            yield 1.0
        self.remove([doer])
        self.remove(self.toRemove)

if __name__ == "__main__":

    agent = Agent(name='watcher', bran='HCJhWE8E9DTP69BI1Kdk1')
    agent.initWallet()
    # res = agent.resolveOobi(oobiAlias="dev01",oobi='https://witness-dev01.rootsid.cloud/oobi/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx/controller')
    # print(res)
    agent.queryAID('EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9')


