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

## 4. Deployment Timing: Why No Address Is Published Here

This repository intentionally does not hard-code or publish a deployed contract address. The wallet credentials used to pay for gas and deploy `UselessToken42` are handed to the corrector directly during the evaluation, and the contract is deployed live at that time using the TUI described in `3_deployment_guide.md`. This ensures the evaluator observes the actual compile-and-deploy process end-to-end, instead of only verifying a contract that already exists on-chain.

## 5. Security: Ownership & Privileges

`UselessToken42` deliberately has **no owner and no privileged role**. The contract does not inherit `Ownable`, and it does not expose `mint()`, `pause()`, `blacklist()`, or any other admin-gated function beyond what the plain OpenZeppelin `ERC20` implementation already provides.

**Why no admin controls?**
* **No privileged actor to compromise:** since there is no owner key, there is nothing an attacker (or a careless deployer) can abuse to mint extra supply, freeze balances, or rug-pull holders.
* **Trust minimization:** holders only need to trust the immutable, audited OpenZeppelin `ERC20` logic — not a human with special rights over the contract.
* **Matches the fixed-supply design:** since the entire 42-token supply is minted once in the constructor, there is no legitimate future need for a minting privilege, so the attack surface is simply removed rather than access-controlled.

The trade-off is that this also means **no recovery mechanism** exists (no pause, no blacklist, no upgrade path) — a deliberate choice appropriate for a fixed-supply demo token, but one that would need revisiting for a production asset with regulatory or operational requirements.

## 6. Deployment Tooling & Stack

Rather than relying on heavy frameworks like Hardhat or Foundry, we opted for a custom, Python-driven deployment pipeline.

* **web3.py:** The core library used to connect to the Sepolia RPC node, read blockchain data, construct transactions, and sign them locally using the deployer's private key.
* **py-solc-x:** Used to dynamically compile the Solidity (`.sol`) smart contract into the ABI and EVM Bytecode required for deployment directly from the Python script.
* **Rich:** Used to build a clean, responsive Terminal User Interface (TUI) that guides the user through the compilation and deployment lifecycle.
