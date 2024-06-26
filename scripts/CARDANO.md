This implementation depends on [Blockfrost](https://blockfrost.io) to interact to cardano. In order to use this implementation and run the demos you need to create an account, create a project and get an API KEY. For demo purposes you can create one project on a Free Tier and use a testnet network such as `Preview`.

## Getting started
- add your blockfrost API KEY to the environment variable `BLOCKFROST_API_KEY`
```
export BLOCKFROST_API_KEY={Your API KEY}
```
- install dependencies
```
pip install -r requirements.txt
```
-  create a Cardano Address
```
python cardano_agent.py cardano_address
```
- fund your address with test ADA from [Testnets faucet](https://docs.cardano.org/cardano-testnet/tools/faucet)
- add the private key the environmental variable `CARDANO_ADDRESS_CBORHEX`. This step is just for demo purposes with test ADA. Storing a private key in an environmental variable is highly insecure!!!
```
export CARDANO_ADDRESS_CBORHEX={ CBORHex }
```
- You can view transactions in the blockchain with [Cardano Scan](https://preview.cardanoscan.io)