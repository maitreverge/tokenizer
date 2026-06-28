// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.35;

// We inherit from OpenZeppelin's audited, battle-tested ERC20 implementation.
// This gives us transfer(), balanceOf(), approve(), totalSupply(), etc. for free.
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title Token42
 * @notice A simple ERC-20 token created for the 42 Tokenizer project.
 * @dev    Inherits the full ERC20 standard. The entire initial supply is
 *         minted to the deployer, who can then distribute it to other wallets.
 */
contract Token42 is ERC20 {
    /**
     * @notice Creates the token and mints the initial supply to the deployer.
     * @dev    `_mint` is called only once, in the constructor, so the supply
     *         is fixed at deployment (no inflation possible afterwards).
     *         Amount is expressed in the smallest unit (wei-like, 18 decimals).
     */
    constructor() ERC20("Token42", "T42") {
        // Mint 42 tokens (with 18 decimals) to whoever deploys the contract.
        _mint(msg.sender, 42 * 10 ** decimals());
    }

    /**
    * @notice Trivial view function used as a liveness/smoke-test:
    *         proves the deployed contract is reachable and responds to calls.
    * @return A constant greeting string.
    */
    function helloWorld() external pure returns (string memory) {
        return "Hello, World!";
    }
}
