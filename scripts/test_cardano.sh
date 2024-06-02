# DEMO TEST
# Requirements:
# Run cardano watcher (python main.py)
# Run a MongoDB instance (docker run -d -p 27017:27017 mongo)
# A cardano testnet  address as CBORHEX in env CARDANO_ADDRESS_CBORHEX (you can execute "python cardano_agent.py cardano_address")
# A Blockfrost API key in env BLOCKFROST_API_KEY
# Fund your cardano address (https://docs.cardano.org/cardano-testnet/tools/faucet)


python cardano_agent.py init cardano
python cardano_agent.py incept cardano aid1

python cardano_agent.py rotate cardano aid1