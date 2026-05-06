// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.35;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Base contract inherits fromthe standart ERC20 object
contract Token_42_Base is ERC20 {
      constructor() ERC20("Token_hello", "T4H_Coin") {
        // de base c'est en wei (Gas Gwei = Gwei)
        _mint(msg.sender, 142 * 10**18);
    }
    // fonction burn pour bruler des tokens
}