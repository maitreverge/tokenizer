// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.35;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Base contract inherits fromthe standart ERC20 object
contract Token_42_Base is ERC20 {
      constructor() ERC20("Another Useless Token", "AUT") {
        // de base c'est en wei (Gas Gwei = Gwei)
        _mint(msg.sender, 42 * 10**18);
    }
    
    // Basic function to interact with the token
    function helloWorld() public pure returns (string memory) {
        return "Hello From Smart Contract -Another Useless Token-";
    }
}