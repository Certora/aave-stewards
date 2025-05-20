
using ERC20A as erc20a;

methods {
  function COLLECTOR() external returns(address) envfree;
  function priceChecker() external returns(address) envfree;
  function limitOrderPriceChecker() external returns(address) envfree;
  function erc20a.balanceOf(address account) external returns (uint256) envfree;

  function _.transfer(address to, uint256 value) external => DISPATCHER(true);
  function _.transferFrom(address from, address to, uint256 value) external => DISPATCHER(true);
  function _.approve(address spender, uint256 amount) external => DISPATCHER(true);
  function _.balanceOf(address account) external => DISPATCHER(true);
  function _.allowance(address owner, address spender) external => DISPATCHER(true);

  //function _.safeTransfer(address to, uint256 value) external => DISPATCHER(true);
  //function _.safeTransferFrom(address from, address to, uint256 value) external => DISPATCHER(true);
  //function _.balanceOf(address usr) external => DISPATCHER(true);
  //  function _.decimals() external => DISPATCHER(true);
}


// *************************************************************************************************
// Summarizations
// *************************************************************************************************

methods {
  function _.getExpectedOut(uint256 _amountIn, address _fromToken, address _toToken, bytes _data)
    external => NONDET;

  function _.decimals() external => NONDET;
  
  function _.remove(bytes32) external => NONDET;
  function _.singleOrders(address user, bytes32 _hash) external => NONDET;
  function _.create(IConditionalOrder.ConditionalOrderParams params, bool dispatch) external => NONDET;

  function _.cancelSwap(uint256 amountIn,
                        address fromToken,
                        address toToken,
                        address to,
                        bytes32 appData,
                        address priceChecker,
                        bytes priceCheckerData
                       ) external
    => CVL_cancelSwap(calledContract/*tradeMilkman*/, amountIn, fromToken, toToken, to, priceChecker) expect void;
  
  function _.requestSwapExactTokensForTokens(uint256 amountIn,
                                             address fromToken,
                                             address toToken,
                                             address to,
                                             bytes32 appData,
                                             address priceChecker,
                                             bytes  priceCheckerData
                                            ) external
    => CVL_requestSwapExactTokensForTokens(amountIn,fromToken,toToken,to,priceChecker) expect void;
}


persistent ghost address __cancelSwap_PRM_tradeMilkman;
persistent ghost uint256 __cancelSwap_PRM_amountIn;
persistent ghost address __cancelSwap_PRM_fromToken;
persistent ghost address __cancelSwap_PRM_toToken;
persistent ghost address __cancelSwap_PRM_to;
persistent ghost address __cancelSwap_PRM_priceChecker;

function CVL_cancelSwap(address tradeMilkman,
                        uint256 amountIn,
                        address fromToken,
                        address toToken,
                        address to,
                        address priceChecker
                       ) {
  __cancelSwap_PRM_tradeMilkman = tradeMilkman;
  __cancelSwap_PRM_amountIn = amountIn;
  __cancelSwap_PRM_fromToken = fromToken;
  __cancelSwap_PRM_toToken = toToken;
  __cancelSwap_PRM_to = to;
  __cancelSwap_PRM_priceChecker = priceChecker;
}




persistent ghost uint256 __requestSwap_PRM_amountIn;
persistent ghost address __requestSwap_PRM_fromToken;
persistent ghost address __requestSwap_PRM_toToken;
persistent ghost address __requestSwap_PRM_to;
persistent ghost address __requestSwap_PRM_priceChecker;

function CVL_requestSwapExactTokensForTokens(uint256 amountIn,
                                            address fromToken,
                                            address toToken,
                                            address to,
                                            address priceChecker) {
  __requestSwap_PRM_amountIn = amountIn;
  __requestSwap_PRM_fromToken = fromToken;
  __requestSwap_PRM_toToken = toToken;
  __requestSwap_PRM_to = to;
  __requestSwap_PRM_priceChecker = priceChecker;
}




rule sanity(method f) filtered {f -> f.contract==currentContract}
{
  env e;
  calldataarg arg;
  f(e, arg);
  satisfy true;
}




// *************************************************************************************************
// Rule: swap_params_correctness
// *************************************************************************************************
rule swap_params_correctness() {
  __requestSwap_PRM_amountIn = 0;
  __requestSwap_PRM_fromToken = 0;
  __requestSwap_PRM_toToken = 0;
  __requestSwap_PRM_to = 0;
  __requestSwap_PRM_priceChecker = 0;
  
  address fromToken; address toToken; uint256 amount; uint256 slippage;
  env e;

  swap(e, fromToken, toToken, amount, slippage);

  assert __requestSwap_PRM_amountIn <= amount;
  assert __requestSwap_PRM_fromToken == fromToken;
  assert __requestSwap_PRM_toToken == toToken;
  assert __requestSwap_PRM_to == COLLECTOR();
  assert __requestSwap_PRM_priceChecker == priceChecker();
}


// *************************************************************************************************
// Rule: limitSwap_params_correctness
// *************************************************************************************************
rule limitSwap_params_correctness() {
  __requestSwap_PRM_amountIn = 0;
  __requestSwap_PRM_fromToken = 0;
  __requestSwap_PRM_toToken = 0;
  __requestSwap_PRM_to = 0;
  __requestSwap_PRM_priceChecker = 0;
  
  address fromToken; address toToken; uint256 amount; uint256 amountOut;
  env e;

  limitSwap(e, fromToken, toToken, amount, amountOut);

  assert __requestSwap_PRM_amountIn <= amount;
  assert __requestSwap_PRM_fromToken == fromToken;
  assert __requestSwap_PRM_toToken == toToken;
  assert __requestSwap_PRM_to == COLLECTOR();
  assert __requestSwap_PRM_priceChecker == limitOrderPriceChecker();
}


// *************************************************************************************************
// Rule: cancelSwap_params_correctness
// *************************************************************************************************
rule cancelSwap_params_correctness() {
  __cancelSwap_PRM_tradeMilkman = 0;
  __cancelSwap_PRM_amountIn = 0;
  __cancelSwap_PRM_fromToken = 0;
  __cancelSwap_PRM_toToken = 0;
  __cancelSwap_PRM_to = 0;
  __cancelSwap_PRM_priceChecker = 0;
  
  address tradeMilkman; address fromToken; address toToken; uint256 amount; uint256 slippage;
  env e;

  cancelSwap(e, tradeMilkman, fromToken, toToken, amount, slippage);

  assert __cancelSwap_PRM_tradeMilkman == tradeMilkman;
  assert __cancelSwap_PRM_amountIn == amount;
  assert __cancelSwap_PRM_fromToken == fromToken;
  assert __cancelSwap_PRM_toToken == toToken;
  assert __cancelSwap_PRM_to == COLLECTOR();
  assert __cancelSwap_PRM_priceChecker == priceChecker();
}



// *************************************************************************************************
// Rule: cancelLimitSwap_params_correctness
// *************************************************************************************************
rule cancelLimitSwap_params_correctness() {
  __cancelSwap_PRM_tradeMilkman = 0;
  __cancelSwap_PRM_amountIn = 0;
  __cancelSwap_PRM_fromToken = 0;
  __cancelSwap_PRM_toToken = 0;
  __cancelSwap_PRM_to = 0;
  __cancelSwap_PRM_priceChecker = 0;
  
  address tradeMilkman; address fromToken; address toToken; uint256 amount; uint256 amountOut;
  env e;

  cancelLimitSwap(e, tradeMilkman, fromToken, toToken, amount, amountOut);

  assert __cancelSwap_PRM_tradeMilkman == tradeMilkman;
  assert __cancelSwap_PRM_amountIn == amount;
  assert __cancelSwap_PRM_fromToken == fromToken;
  assert __cancelSwap_PRM_toToken == toToken;
  assert __cancelSwap_PRM_to == COLLECTOR();
  assert __cancelSwap_PRM_priceChecker == limitOrderPriceChecker();
}


definition is_swap(method f) returns bool =
  f.selector == sig:swap(address,address,uint256,uint256).selector;
definition is_limitSwap(method f) returns bool =
  f.selector == sig:limitSwap(address,address,uint256,uint256).selector;
definition is_twapSwap(method f) returns bool =
  f.selector == sig:twapSwap(address,address,uint256,uint256,uint256,uint256,uint256,uint256).selector;

definition is_cancelSwap(method f) returns bool =
  f.selector == sig:cancelSwap(address,address,address,uint256,uint256).selector;
definition is_cancelLimitSwap(method f) returns bool =
  f.selector == sig:cancelLimitSwap(address,address,address,uint256,uint256).selector;
definition is_cancelTwapSwap(method f) returns bool =
  f.selector == sig:cancelTwapSwap(address,address,uint256,uint256,uint256,uint256,uint256,uint256,uint256).selector;

definition is_rescueToken(method f) returns bool =
  f.selector == sig:rescueToken(address).selector;



rule balanceOf_COLLECTER_doesnt_decrease_by_more_than_amount(method f) filtered {f ->
    is_swap(f)
    || is_limitSwap(f)
    || is_twapSwap(f)
    }
{
  address fromToken; address toToken; uint256 amount; uint256 slippage;
  uint256 partSellAmount; uint256 minPartLimit; uint256 startTime; uint256 numParts; uint256 partDuration; uint256 span;
  env e;

  uint256 bal_before = erc20a.balanceOf(COLLECTOR());
  
  if (is_swap(f))
    swap(e, erc20a, toToken, amount, slippage);
  else if (is_limitSwap(f))
    limitSwap(e, erc20a, toToken, amount, slippage);
  else if (is_twapSwap(f)) {
    twapSwap(e, fromToken, toToken, partSellAmount, minPartLimit, startTime, numParts, partDuration, span);
  }

  mathint the_amount = is_twapSwap(f) ? partSellAmount * numParts : amount;

  uint256 bal_after = erc20a.balanceOf(COLLECTOR());

  assert bal_after >= bal_before - the_amount;
}



rule only_swap_functions_can_decrease_balanceOf_COLLECTER(method f) filtered {f->
    f.contract == currentContract
    }
{
  address fromToken; address toToken; uint256 amount; uint256 slippage;
  uint256 partSellAmount; uint256 minPartLimit; uint256 startTime; uint256 numParts; uint256 partDuration; uint256 span;
  env e;
  calldataarg args;
  
  uint256 bal_before = erc20a.balanceOf(COLLECTOR());

  f(e,args);

  uint256 bal_after = erc20a.balanceOf(COLLECTOR());

  assert bal_after < bal_before => (is_swap(f) || is_limitSwap(f) || is_twapSwap(f));
}



rule only_cancel_functions_can_increase_balanceOf_COLLECTER(method f) filtered {f->
    f.contract == currentContract
    }
{
  address fromToken; address toToken; uint256 amount; uint256 slippage;
  uint256 partSellAmount; uint256 minPartLimit; uint256 startTime; uint256 numParts; uint256 partDuration; uint256 span;
  env e;
  calldataarg args;
  
  uint256 bal_before = erc20a.balanceOf(COLLECTOR());

  f(e,args);

  uint256 bal_after = erc20a.balanceOf(COLLECTOR());

  assert bal_after > bal_before => (is_cancelSwap(f) || is_cancelLimitSwap(f) || is_cancelTwapSwap(f) || is_rescueToken(f));
}










rule temp() {
  address tradeMilkman; address fromToken; address toToken; uint256 amount; uint256 slippage;
  env e;   calldataarg args;

  
  uint256 bal_before = erc20a.balanceOf(COLLECTOR());

  cancelTwapSwap(e, args);

  uint256 bal_after = erc20a.balanceOf(COLLECTOR());

  assert bal_after >= bal_before;
}

