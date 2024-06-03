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
from keri.core.eventing import Siger, Kevery
from keri.core.parsing import Parser
from keri.core import serdering
from keri.kering import sniff, Version
from keri.core.coring import Counter
from keri.end import ending

from store import get_aid, store_aid, store_kel, get_kel

class Agent:
    def __init__(self, name, bran):
        self.bran = bran
        self.name = name
        self.hby = None

    def initWallet(self):
        kwa = dict()
        kwa["bran"] = self.bran
        self.hby = habbing.Habery(name=self.name, **kwa)
        rgy = credentialing.Regery(hby=self.hby, name=self.name)

        print("KERI Keystore created at:", self.hby.ks.path)
        print("KERI Database created at:", self.hby.db.path)
        print("KERI Credential Store created at:", rgy.reger.path)
        try:
            hab = self.hby.makeHab(name=self.name)
        except:
            hab = self.hby.habByName(self.name)
        print(f'Watcher AID {hab.pre}')

    def createAidForWitness(self, witness_pre):
        hab = self.hby.makeHab(name='for-witness-' + witness_pre, transferable=True, icount=1, ncount=1,isith=1,nsith=1, toad=1, wits=[witness_pre])
        return hab.pre

    def resolveOobi(self, alias, oobi):
        doers = [OobiDoer(name=self.name, oobi=oobi, oobiAlias=alias, hby = self.hby)]
        directing.runController(doers=doers, expire=5.0)
        obr = self.hby.db.roobi.get(keys=(oobi,))
        if obr:
            prefix = obr.cid
            kever = self.hby.kevers[prefix]
            cloner = self.hby.db.clonePreIter(pre=prefix, fn=0)  # create iterator at 0
            for msg in cloner:
                srdr = serdering.SerderKERI(raw=msg)
                store_kel(prefix, srdr.sn, msg.decode("utf-8"))
            return prefix
        else:
            return None
        
    def queryAID(self, prefix):
        aid = get_aid(prefix)
        kever = self.hby.kevers[aid['prefix']]
        wits = kever.wits
        # TODO search for a known witness
        alias = 'for-witness-' + wits[0]
        doers = [QueryDoer(name=self.name, alias=alias,hby=self.hby, pre=prefix)]
        directing.runController(doers=doers, expire=0.0)

        return 
        
    def watchAID(self, prefix):
        aid = get_aid(prefix)
        if aid:
            if not aid['cardano']:
                self.resolveOobi(alias=aid['alias'], oobi=aid['oobi'])
            return get_kel(prefix)
        else:
            return []
        
    def parseMsg(self, msg):
        kvy = Kevery(db=self.hby.db, lax=True, local=False)
        parser = Parser(framed=True, kvy=kvy)
        parser.parse(ims=bytearray(msg, encoding='utf8'))

        serdery = serdering.Serdery(version=Version)
        try:
            serder = serdery.reap(ims=bytearray(msg, encoding='utf8'))
            if not get_aid(serder.pre):
                aid = {
                    "prefix": serder.pre,
                    "alias": serder.pre,
                    "cardano": True,
                    "watched": True,
                    'oobi': 'NA'
                }
                store_aid(aid)
                print("New AID discovered on Cardano", serder.pre)

            cloner = self.hby.db.clonePreIter(pre=serder.pre, fn=0)  # create iterator at 0
            for msg in cloner:
                srdr = serdering.SerderKERI(raw=msg)
                store_kel(serder.pre, srdr.sn, msg.decode("utf-8"))

        except Exception as e:
            print(e)

    def printPre(self, prefix):
        kever = self.hby.kevers[prefix]
        ser = kever.serder
        print("{}: {}".format('AID', prefix))
        print("Seq No:\t{}".format(kever.sner.num))
        cloner = self.hby.db.clonePreIter(pre=prefix, fn=0)  # create iterator at 0
        for msg in cloner:
            print(msg)
            srdr = serdering.SerderKERI(raw=msg)
            print(srdr.pretty())
            print()

    def verifyHeaders(self, request):
        headers = request.headers
        if "SIGNATURE-INPUT" not in headers or "SIGNATURE" not in headers:
            return False

        siginput = headers["SIGNATURE-INPUT"]
        if not siginput:
            return False
        signature = headers["SIGNATURE"]
        if not signature:
            return False
        
        resource = headers["Signify-Resource"]
        if not resource:
            return False

        inputs = ending.desiginput(siginput.encode("utf-8"))
        inputs = [i for i in inputs if i.name == "signify"]

        if not inputs:
            return False

        for inputage in inputs:
            items = []
            for field in inputage.fields:
                if field.startswith("@"):
                    if field == "@method":
                        items.append(f'"{field}": {request.method}')
                    elif field == "@path":
                        items.append(f'"{field}": {request.url.path}')

                else:
                    key = field.upper()
                    field = field.lower()
                    if key not in headers:
                        continue

                    value = ending.normalize(headers[key])
                    items.append(f'"{field}": {value}')

            values = [f"({' '.join(inputage.fields)})", f"created={inputage.created}"]
            if inputage.expires is not None:
                values.append(f"expires={inputage.expires}")
            if inputage.nonce is not None:
                values.append(f"nonce={inputage.nonce}")
            if inputage.keyid is not None:
                values.append(f"keyid={inputage.keyid}")
            if inputage.context is not None:
                values.append(f"context={inputage.context}")
            if inputage.alg is not None:
                values.append(f"alg={inputage.alg}")

            params = ';'.join(values)

            items.append(f'"@signature-params: {params}"')
            ser = "\n".join(items).encode("utf-8")

            # resource = self.resource(request)
            # agent = self.agency.get(resource)

            # if agent is None:
            #     raise kering.AuthNError("unknown or invalid controller")

            # if resource not in agent.agentHab.kevers:
            #     raise kering.AuthNError("unknown or invalid controller")

            ckever = kever = self.hby.kevers[resource]
            signages = ending.designature(signature)
            cig = signages[0].markers[inputage.name]
            if not ckever.verfers[0].verify(sig=cig.raw, ser=ser):
                return False

        return True

class OobiDoer(doing.DoDoer):
    """ DoDoer for loading oobis and waiting for the results """

    def __init__(self, name, oobi, oobiAlias, hby):

        self.processed = 0
        self.oobi = oobi
        self.hby = hby
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

    def __init__(self, alias, hby, pre, **kwa):
        doers = []
        self.hby = hby
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
    # agent.queryAID('EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9')
    # agent.printPre('EC12CJHxS0Dys74Uko2vFUMxXULPx3WcLoIIQzOFsnMH')
    agent.printPre('EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9')
