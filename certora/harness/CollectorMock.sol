
import {Address} from 'openzeppelin-contracts/contracts/utils/Address.sol';
import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';


contract CollectorMock {
  using Address for address payable;

  address public constant ETH_MOCK_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

  function transfer(IERC20 token, address recipient, uint256 amount) external {
    require (recipient != address(0));

    if (address(token) == ETH_MOCK_ADDRESS) {
      payable(recipient).sendValue(amount);
    } else {
      token.transfer(recipient, amount);
    }
  }




}
