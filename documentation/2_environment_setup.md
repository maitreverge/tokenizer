# Environment Setup & Prerequisites

Before compiling and deploying the smart contract, you must configure your local environment and prepare your blockchain credentials. This guide walks you through the setup process.

## 1. Local Dependencies

As outlined in the main `README.md`, the project relies on a specific local setup to manage dependencies. All of them are managed by the Dockerfile and `docker-compose.yml` configuration.

```bash
# Build the Docker image
docker compose build
```

```bash
# Run the container and open a shell inside it
docker compose run --rm tokenizer
```

## 2. Environment Configuration (.env)

The deployment scripts rely on a `.env` file to securely load your credentials and network settings.

Copy the provided template to create your configuration file:

```bash
cp deployment/.env.example deployment/.env
```

#### Configuration Variables Breakdown

Open the .env file and configure the following variables:

- `SEPOLIA_ENTRYPOINT`: The RPC (Remote Procedure Call) URL used to communicate with the Sepolia blockchain.
  Default: A public node is provided, but it is highly recommended to create a free account on providers like Alchemy or Infura to get a reliable, private RPC URL.
- `SMART_CONTRACT_PATH`: The path to the Solidity file. Leave as default (../code/contract/contract.sol) unless you change the repository structure.
- `WALLETS_FILE`: Path for the wallet manager to store generated wallets.
- `CONTRACT_ADDRESS`: Leave this empty for now. You will populate this variable after successfully running the deployment script.
- `MY_PRIVATE_KEY`: The private key associated with your public key. This is strictly required to locally sign the deployment transaction.
- `MY_PUBLIC_KEY`: Your Ethereum wallet address (e.g., 0x123...).


## 3. Blockchain Prerequisites: Gas and Faucets

Every operation that modifies the state of the blockchain (_like deploying a smart contract or transferring tokens_) requires a computation fee known as **Gas**.

**Gas** is paid in the native currency of the network—in this case, _**Sepolia ETH**_.

To deploy `UselessToken42`, the wallet associated with `MY_PRIVATE_KEY` must have a positive balance of Sepolia ETH.

### How to get Sepolia ETH:

Since Sepolia is a testnet, ETH is free and distributed via "Faucets". You can request testnet funds from the following reliable sources:

- Alchemy Sepolia Faucet (Requires an Alchemy account)
- QuickNode Sepolia Faucet
- Infura Faucet

Enter your `MY_PUBLIC_KEY` address into one of these faucets to receive the test ETH.

You can verify your balance by looking up your address on the Sepolia Etherscan Block Explorer.

Once your `.env` is configured and your wallet is funded, you are ready to deploy the contract.
