// SPDX-License-Identifier: GPL-3.0
// The `^` indicates => Version 0.8.26 or newer
pragma solidity ^0.8.26;

// This will only compile via IR
// In the contract lives the core logic of the whole Smart Contract.

// Naming conventions => must match the name of the file
contract Coin {
    
    // Variable of type adress (a wallet, another smart contract).
    // This adress indicates the adress of who is allowed to mint (create) coins.
    address public minter;

    // Creating a hashmap of who own hoe much tokens 
    /*
    0xABC...        => 1000
    0xDEF...        => 500
    
    */
    // This variable balances mus be updated manually, as nothing is automatic
    // ! This is also mandatory by ERC-20 standart

    // ? Note : adding `public` to this automatically create a function `balances(adress)` to
    // ? publicly access the tokens o a specify wallet
    mapping(address => uint) public balances;

    // Events allow clients to react to specific
    // contract changes you declare
    event Sent(address from, address to, uint amount);

    /*
    ! msg.sender is a built-in Solidity variable that always refers
    ! to the address that triggered the current call — in this case, you, the deployer.
    
    The constructor runs at deployment time —
    the moment you publish your contract to the blockchain. That's it, never again.
    */
    constructor() {
        minter = msg.sender;
    }

    // Sends an amount of newly created coins to an address
    // Can only be called by the contract creator
    function mint(address receiver, uint amount) public {
        require(msg.sender == minter);
        balances[receiver] += amount;
    }

    // Errors allow you to provide information about
    // why an operation failed. They are returned
    // to the caller of the function.
    error InsufficientBalance(uint requested, uint available);

    // Sends an amount of existing coins
    // from any caller to an address
    function send(address receiver, uint amount) public {
        require(amount <= balances[msg.sender], InsufficientBalance(amount, balances[msg.sender]));
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Sent(msg.sender, receiver, amount);
    }
}