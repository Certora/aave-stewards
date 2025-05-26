// SPDX-License-Identifier: agpl-3.0
pragma solidity >=0.8.20;

//import { ERC20 } from 'openzeppelin-contracts/contracts/token/ERC20/ERC20.sol';
import {ERC20Impl} from 'certora/harness/erc20/ERC20Impl.sol';

contract ERC20A is ERC20Impl {
  constructor() ERC20Impl() {}
}
