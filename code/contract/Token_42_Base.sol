// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.26;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Base contract inherits fromthe standart ERC20 object
contract Token_42_Base is ERC20 {
      constructor() ERC20("Token_42_Base", "T4B") {
        _mint(msg.sender, 4242);
    }
}