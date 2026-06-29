# Wallet Management & Token Interaction

Now that your smart contract is deployed on the Sepolia testnet and your `CONTRACT_ADDRESS` is safely stored in your `.env` file, you have full control over your newly minted tokens. 

To make interacting with your tokens easy and intuitive, this repository includes a dedicated interactive tool: `wallet_manager.py`.

## 1. Launching the Wallet Manager

Ensure your Python virtual environment is active (via `source ./p_env.sh master`), then launch the interactive script:

```bash
python wallet_manager.py
```

This script provides a command-line interface designed to give you complete, hands-on control over your token ecosystem.

## 2. Features overview

The Wallet Manager includes several built-in features to test your token's functionality without needing to write custom scripts or use external platforms:
-  Generate Wallets on the Fly

You can instantly generate new Ethereum wallets directly from the interface. This is perfect for creating test accounts to simulate a real user base for your token.
-  Refresh & View Balances

The manager connects seamlessly to the Sepolia blockchain to fetch real-time data. You can instantly check the balances of both:

Sepolia ETH: To ensure a wallet has enough gas for transactions.
Your Custom Token: To track who holds your newly created token.

-  Manage Credentials

The interface provides quick options to copy public addresses and private keys of the wallets you generate. 
(Note: These are meant for testnet purposes. Do not use these generated wallets for real funds on the Ethereum Mainnet.)

## 3. Simulating Transactions (Next Steps)

With the Wallet Manager, you can create a network of test wallets. A typical testing workflow looks like this:

- Generate two or three new wallets using the script.
- Fund them with a tiny amount of Sepolia ETH (using faucets or sending from your deployer wallet) so they can pay for gas.
- Transfer some of your custom tokens from your main deployer wallet to these newly generated addresses.
- Refresh the balances in the Wallet Manager to watch the on-chain transactions update in real-time.

By using contract_uploader.py to deploy and wallet_manager.py to interact, you have successfully built and managed your own cryptocurrency ecosystem!