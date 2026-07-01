# Technical Choices & Architecture

This document outlines the core architectural and technical decisions made for the Tokenizer project. 

## 1. The Blockchain: Ethereum (Sepolia Testnet)

For this project, we chose to deploy our smart contract on the **Sepolia** test network. 

**Why Sepolia?**
* **Standard Development Environment:** Sepolia is the recommended and primary testnet for Ethereum application development following the Merge. 
* **Proof-of-Stake:** It mirrors the current Proof-of-Stake (PoS) consensus mechanism of the Ethereum Mainnet, providing a highly accurate testing environment.
* **Accessibility:** Testnet ETH (Sepolia ETH) is readily available via various public endpoints, which is strictly required to pay for the "gas" fees associated with deploying the contract and executing transactions.

## 2. The Token Standard: ERC-20

Our token, `UselessToken42` (UT42), is built upon the **ERC-20** standard. 

**What is ERC-20?**
ERC-20 (Ethereum Request for Comments 20) is the universally accepted technical standard for **fungible tokens** created using smart contracts on the Ethereum blockchain. "Fungible" means that every token is exactly the same in type and value as any other token (like fiat currency).

**Why use it?**
Implementing the ERC-20 standard ensures **interoperability**. Because our contract adheres strictly to the ERC-20 interface, any standard Ethereum wallet (like MetaMask) or decentralized application knows exactly how to read the token's balance, transfer it, and approve third-party spending, without needing custom integration logic.

## 3. Smart Contract Implementation: OpenZeppelin

Writing a secure smart contract from scratch is highly risky due to the immutable nature of blockchains. To ensure maximum security and reliability, we utilized the **OpenZeppelin** library.

* **Inheritance:** Our contract inherits from OpenZeppelin’s audited, battle-tested `ERC20.sol` implementation. This provides us with highly secure, optimized versions of standard functions (`transfer()`, `balanceOf()`, `approve()`, etc.) out of the box.
* **Tokenomics:** The supply is hardcoded and fixed at deployment. In the constructor, we mint exactly 42 tokens (multiplied by $10^{18}$ to account for the standard 18 decimal places) directly to the deployer's address. No further inflation or minting is possible.

## 4. Deployment Tooling & Stack

Rather than relying on heavy frameworks like Hardhat or Foundry, we opted for a custom, Python-driven deployment pipeline.

* **web3.py:** The core library used to connect to the Sepolia RPC node, read blockchain data, construct transactions, and sign them locally using the deployer's private key.
* **py-solc-x:** Used to dynamically compile the Solidity (`.sol`) smart contract into the ABI and EVM Bytecode required for deployment directly from the Python script.
* **Rich:** Used to build a clean, responsive Terminal User Interface (TUI) that guides the user through the compilation and deployment lifecycle.
