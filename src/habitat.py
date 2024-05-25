from hio import help
from hio.base import doing

from keri.app import directing

import keri.app.oobiing
from keri.app import habbing, configing, oobiing, indirecting, delegating, forwarding, agenting
from keri.app.keeping import Algos
from keri.kering import ConfigurationError
from keri.vdr import credentialing
from keri.app.cli.common import existing, incepting, config



class InitDoer(doing.DoDoer):

    def __init__(self, args):
        self.args = args
        super(InitDoer, self).__init__(doers=[doing.doify(self.initialize)])

    def initialize(self, tymth, tock=0.0):
        # enter context
        self.wind(tymth)
        self.tock = tock
        _ = (yield self.tock)

        args = self.args
        name = args['name']
        if name is None or name == "":
            raise ConfigurationError("Name is required and can not be empty")

        base = args['base']
        temp = args['temp']
        bran = args['bran']
        configFile = args['configFile']
        configDir = args['configDir']

        if not args['nopasscode'] and not bran:
            raise ConfigurationError("Bran is required when passcode is not provided")

        kwa = dict()
        kwa["salt"] = args['salt']
        kwa["bran"] = bran
        kwa["aeid"] = args['aeid']
        kwa["seed"] = args['seed']
        if args['salt'] is None:
            kwa["algo"] = Algos.randy

        cf = None
        if configFile is not None:
            cf = configing.Configer(name=configFile,
                                    base="",
                                    headDirPath=configDir,
                                    temp=False,
                                    reopen=True,
                                    clear=False)

        hby = habbing.Habery(name=name, base=base, temp=temp, cf=cf, **kwa)
        rgy = credentialing.Regery(hby=hby, name=name, base=base, temp=temp)

        print("KERI Keystore created at:", hby.ks.path)
        print("KERI Database created at:", hby.db.path)
        print("KERI Credential Store created at:", rgy.reger.path)
        if hby.mgr.aeid:
            print("\taeid:", hby.mgr.aeid)

        oc = hby.db.oobis.cntAll()
        if oc:
            print(f"\nLoading {oc} OOBIs...")

            obi = keri.app.oobiing.Oobiery(hby=hby)
            self.extend(obi.doers)

            while oc > hby.db.roobi.cntAll():
                yield 0.25

            for (oobi,), obr in hby.db.roobi.getItemIter():
                if obr.state in (oobiing.Result.resolved,):
                    print(oobi, "succeeded")
                if obr in (oobiing.Result.failed,):
                    print(oobi, "failed")

            self.remove(obi.doers)

        wc = [oobi for (oobi,), _ in hby.db.woobi.getItemIter()]
        if len(wc) > 0:
            print(f"\nAuthenticating Well-Knowns...")
            authn = oobiing.Authenticator(hby=hby)
            self.extend(authn.doers)

            while True:
                cap = []
                for (_,), wk in hby.db.wkas.getItemIter(keys=b''):
                    cap.append(wk.url)

                if set(wc) & set(cap) == set(wc):
                    break

                yield 0.5

            self.remove(authn.doers)

        hby.close()
        
class InceptDoer(doing.DoDoer):
    """ DoDoer for creating a new identifier prefix and Hab with an alias.
    """

    def __init__(self, name, base, alias, bran, endpoint, proxy=None, cnfg=None, **kwa):

        cf = None
        # if config is not None:
        #     cf = configing.Configer(name=name,
        #                             base="",
        #                             headDirPath=cnfg,
        #                             temp=False,
        #                             reopen=True,
        #                             clear=False)
        self.endpoint = endpoint
        self.proxy = proxy
        hby = existing.setupHby(name=name, base=base, bran=bran, cf=cf)
        self.hbyDoer = habbing.HaberyDoer(habery=hby)  # setup doer
        self.swain = delegating.Sealer(hby=hby)
        self.postman = forwarding.Poster(hby=hby)
        self.mbx = indirecting.MailboxDirector(hby=hby, topics=['/receipt', "/replay", "/reply"])
        doers = [self.hbyDoer, self.postman, self.mbx, self.swain, doing.doify(self.inceptDo)]

        self.inits = kwa
        self.alias = alias
        self.hby = hby
        super(InceptDoer, self).__init__(doers=doers)

    def inceptDo(self, tymth, tock=0.0):
        """
        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value

        Returns:  doifiable Doist compatible generator method
        """
        # enter context
        self.wind(tymth)
        self.tock = tock
        _ = (yield self.tock)

        hab = self.hby.makeHab(name=self.alias, **self.inits)
        witDoer = agenting.WitnessReceiptor(hby=self.hby)
        receiptor = agenting.Receiptor(hby=self.hby)
        self.extend([witDoer, receiptor])

        # if hab.kever.delegator:
        #     self.swain.delegation(pre=hab.pre, sn=0, proxy=self.hby.habByName(self.proxy))
        #     print("Waiting for delegation approval...")
        #     while not self.swain.complete(hab.kever.prefixer, coring.Seqner(sn=hab.kever.sn)):
        #         yield self.tock

        if hab.kever.wits:
            print("Waiting for witness receipts...")
            if self.endpoint:
                yield from receiptor.receipt(hab.pre, sn=0)
            else:
                witDoer.msgs.append(dict(pre=hab.pre))
                while not witDoer.cues:
                    _ = yield self.tock

        # if hab.kever.delegator:
        #     yield from self.postman.sendEvent(hab=hab, fn=hab.kever.sn)

        print(f'Prefix  {hab.pre}')
        for idx, verfer in enumerate(hab.kever.verfers):
            print(f'\tPublic key {idx + 1}:  {verfer.qb64}')
        print()

        toRemove = [self.hbyDoer, witDoer, self.mbx, self.swain, self.postman, receiptor]
        self.remove(toRemove)

        return

if __name__ == "__main__":
    args = {
        'name': "test",
        'alias': 'test2',
        'nopasscode': True,
        'bran': None,
        'salt': '0ACH3l7OYPh8MZ9leNXYnHEb',
        'base': '',
        'temp': None,
        'configFile': None,
        'configDir': '',
        'salt': None,
        'aeid': None,
        'seed': None
    }
    doers = [InitDoer(args)]
    directing.runController(doers=doers, expire=0.0)

    icpDoer = [InceptDoer(name=args['name'], base=args['base'], alias=args['alias'], bran=args['bran'], endpoint=None, proxy=None,
                         cnfg=None)]
    directing.runController(doers=icpDoer, expire=0.0)
