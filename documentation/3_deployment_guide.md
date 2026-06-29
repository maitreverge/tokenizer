# Deployment Guide

Once your local environment is configured and your wallet is funded with Sepolia ETH (as covered in `02_environment_setup.md`), you are ready to deploy the `UselessToken42` smart contract to the blockchain.

## 1. Review the Smart Contract (Optional)

Before deploying, you can review the Solidity code located at `code/contract/contract.sol`. 
The token uses the OpenZeppelin ERC-20 standard, which ensures it is secure and fully compliant with the Ethereum token standard. 

Key parameters like the token name (`UselessToken42`), symbol (`UT42`), and initial supply are defined within this file.

## 2. Execute the Deployment Script

The deployment process is automated via a Python script. This script will:
1. Read your credentials and network settings from the `.env` file.
2. Compile the Solidity code into bytecode and an Application Binary Interface (ABI).
3. Create and sign a deployment transaction using your private key.
4. Broadcast the transaction to the Sepolia network and wait for confirmation.

To deploy the contract, navigate to the root of the project and run:

```bash
# Ensure your virtual environment is still active
python code/deployment/deploy.py
```

(Note: Adjust the script path if your deployment script is named differently, such as main.py or located in another directory).

## 3. Save the Contract Address

If the deployment is successful, your terminal will output transaction details, including the newly created Contract Address. It will look something like this:

```
Deploying contract...
Transaction hash: 0xabc123...
Contract deployed successfully!
Contract Address: 0xYourNewContractAddressHere
```

Crucial Step: 
Copy this new contract address, open your `.env` file, and paste it into the `CONTRACT_ADDRESS` variable:

```
CONTRACT_ADDRESS=0xYourNewContractAddressHere
```

Saving this address is required for the interaction scripts (like transferring tokens or checking balances) to know which contract to talk to.

## 4. Verify on Etherscan

You can verify that your contract is live on the blockchain by pasting your new `CONTRACT_ADDRESS` into the Sepolia Etherscan Block Explorer. 

Here, you can see the token tracker, the total supply, and the initial mint transaction that sent all the tokens to your deployer wallet.

**[Optional: Insert a screenshot here of the deployed contract page on Sepolia Etherscan]**