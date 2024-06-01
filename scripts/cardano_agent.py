from keri.app import habbing
from keri.app.cli.common import existing
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from pycardano import * 
from textwrap import wrap
import os
import time

import sys

METADATA_LABEL = int(''.join([str(ord(char) - 96) for char in 'KERIWATCHER'.lower()]))
TRANSACTION_AMOUNT = 1000000
NETWORK = Network.TESTNET
BLOCKFROST_PROJECT_ID = os.environ['BLOCKFROST_API_KEY']
CARDANO_ADDRESS_CBORHEX = os.environ['CARDANO_ADDRESS_CBORHEX']

def init(name):
    kwa = dict()
    hby = habbing.Habery(name=name, **kwa)

    print("KERI Keystore created at:", hby.ks.path)
    print("KERI Database created at:", hby.db.path)

def incept(name, alias):    
    hby = existing.setupHby(name=name)
    hab = hby.makeHab(name=alias)
    print(f'AID: {hab.pre}')
    *_, msg = hab.db.clonePreIter(pre=hab.pre)
    print('KEY event:',msg.decode("utf-8"))
    tx_hash = submitTransaction(msg.decode("utf-8"))
    print(tx_hash)
    hby.close()

def rotate(name, alias):
    hby = existing.setupHby(name=name)
    hab = hby.habByName(alias)
    hab.rotate()
    *_, msg = hab.db.clonePreIter(pre=hab.pre)
    print('KEY event:',msg.decode("utf-8"))
    tx_hash = submitTransaction(msg.decode("utf-8"))
    print(tx_hash)
    hby.close()

def submitTransaction(key_event):
    # Build transaction
    try:
        meta = {
            METADATA_LABEL: wrap(key_event, 64)
        }
        api = BlockFrostApi(
            project_id=BLOCKFROST_PROJECT_ID,
            base_url=ApiUrls.preview.value
        )
        context = BlockFrostChainContext(BLOCKFROST_PROJECT_ID,NETWORK, ApiUrls.preview.value)
        builder = TransactionBuilder(context)
        payment_signing_key = PaymentSigningKey.from_cbor(CARDANO_ADDRESS_CBORHEX)
        payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
        payment_addr = Address(payment_verification_key.hash(), None, network=NETWORK)

        # select utxos
        utxo_sum = 0
        utxo_to_remove = []
        available_utxos = api.address_utxos(payment_addr.encode())
        for u in available_utxos:
            utxo_sum = utxo_sum + int(u.amount[0].quantity)
            builder.add_input(
                UTxO(
                    TransactionInput.from_primitive([u.tx_hash, u.tx_index]),
                    TransactionOutput(address=Address.from_primitive(u.address), amount=int(u.amount[0].quantity))
                )
            )
            utxo_to_remove.append(u)
            if utxo_sum > (TRANSACTION_AMOUNT + 2000000): break
        builder.add_output(TransactionOutput(payment_addr,Value.from_primitive([TRANSACTION_AMOUNT])))
        builder.auxiliary_data = AuxiliaryData(Metadata(meta))
        signed_tx = builder.build_and_sign([payment_signing_key], change_address=payment_addr)
        # Submit transaction
        context.submit_tx(signed_tx.to_cbor())
        return signed_tx.id
    except Exception as e:
        print(e)

def createEnterpriseAddress():
    payment_key_pair = PaymentKeyPair.generate()
    payment_signing_key = payment_key_pair.signing_key
    payment_verification_key = payment_key_pair.verification_key
    payment_address = Address(payment_verification_key.hash(), None, network=NETWORK).encode()

    payment_signing_key = PaymentSigningKey.from_cbor(payment_signing_key.to_cbor())
    payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_addr = Address(payment_verification_key.hash(), None, network=NETWORK)
    print("Enterprise address:", payment_address)
    print("Private Key CBORHex:",payment_signing_key.to_cbor())

if __name__ == "__main__":
    cmd = sys.argv[1]
    name = sys.argv[2]
    if cmd == 'init':
        init(name)
    elif cmd == 'incept':
        incept(name, sys.argv[3])
    elif cmd == 'rotate':
        rotate(name, sys.argv[3])
    elif cmd == 'cardano_address':
        createEnterpriseAddress()
