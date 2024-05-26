from hio import help
from hio.base import doing

from keri.app import directing

import keri.app.oobiing
from keri.app import habbing, configing, oobiing, indirecting, delegating, forwarding, agenting
from keri.app.keeping import Algos
from keri.kering import ConfigurationError
from keri.vdr import credentialing
from keri.app.cli.common import existing, incepting, config
from keri.db import basing
from keri.help import helping

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
            return obr.cid
        else:
            return None

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

        self.extend(self.obi.doers)
        self.extend(self.authn.doers)

        while not self.obi.hby.db.roobi.get(keys=(self.oobi,)):
            yield 0.25

        self.remove([self.hbyDoer, *self.obi.doers, *self.authn.doers]) 

if __name__ == "__main__":

    agent = Agent(name='watcher', bran='HCJhWE8E9DTP69BI1Kdk1')
    agent.initWallet()
    res = agent.resolveOobi(oobiAlias="dev01",oobi='https://witness-dev01.rootsid.cloud/oobi/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx/controller')
    print(res)


