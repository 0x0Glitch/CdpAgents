// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../lib/forge-std/src/Test.sol";
import "../contracts/InterOp.sol";
import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

// Mock USDC token for testing
contract MockUSDC is ERC20 {
    constructor() ERC20("USD Coin", "USDC") {
        _mint(msg.sender, 1000000 * 10**6); // Mint 1M USDC to deployer
    }

    function decimals() public pure override returns (uint8) {
        return 6; // USDC has 6 decimals
    }
}

contract SuperUSDCTest is Test {
    SuperUSDC public superUSDC;
    MockUSDC public usdc;
    
    address public aiAgent;
    address public owner;
    address public user1;
    address public user2;
    
    uint256 public constant INITIAL_BALANCE = 10000 * 10**6; // 10,000 USDC (with 6 decimals)
    
    function setUp() public {
        // Set up accounts
        aiAgent = makeAddr("aiAgent");
        owner = makeAddr("owner");
        user1 = makeAddr("user1");
        user2 = makeAddr("user2");
        
        // Deploy mock USDC
        usdc = new MockUSDC();
        
        // Deploy SuperUSDC contract
        superUSDC = new SuperUSDC(aiAgent, owner, address(usdc));
        
        // Fund user accounts
        usdc.transfer(user1, INITIAL_BALANCE);
        usdc.transfer(user2, INITIAL_BALANCE);
        
        // Approve SuperUSDC to spend user's USDC
        vm.startPrank(user1);
        usdc.approve(address(superUSDC), type(uint256).max);
        vm.stopPrank();
        
        vm.startPrank(user2);
        usdc.approve(address(superUSDC), type(uint256).max);
        vm.stopPrank();
    }
    
    function testDeposit() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDC
        
        vm.startPrank(user1);
        
        // Check balances before deposit
        uint256 initialUSDCBalance = usdc.balanceOf(user1);
        uint256 initialSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Perform deposit
        superUSDC.deposit(depositAmount);
        
        // Check balances after deposit
        uint256 finalUSDCBalance = usdc.balanceOf(user1);
        uint256 finalSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Verify balances
        assertEq(finalUSDCBalance, initialUSDCBalance - depositAmount, "USDC balance should decrease by deposit amount");
        assertEq(finalSuperUSDCBalance, initialSuperUSDCBalance + depositAmount, "SuperUSDC balance should increase by deposit amount");
        
        vm.stopPrank();
    }
    
    function testWithdraw() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDC
        uint256 withdrawAmount = 500 * 10**6; // 500 USDC
        
        // First deposit
        vm.prank(user1);
        superUSDC.deposit(depositAmount);
        
        vm.startPrank(user1);
        
        // Check balances before withdrawal
        uint256 initialUSDCBalance = usdc.balanceOf(user1);
        uint256 initialSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Perform withdrawal
        superUSDC.withdraw(withdrawAmount);
        
        // Check balances after withdrawal
        uint256 finalUSDCBalance = usdc.balanceOf(user1);
        uint256 finalSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Verify balances
        assertEq(finalUSDCBalance, initialUSDCBalance + withdrawAmount, "USDC balance should increase by withdrawal amount");
        assertEq(finalSuperUSDCBalance, initialSuperUSDCBalance - withdrawAmount, "SuperUSDC balance should decrease by withdrawal amount");
        
        vm.stopPrank();
    }
    
    function testCrosschainMint() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDC
        
        // Only aiAgent should be able to crosschain mint
        vm.startPrank(aiAgent);
        
        // Check balance before mint
        uint256 initialSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Perform crosschain mint
        superUSDC.crosschainMint(user1, mintAmount);
        
        // Check balance after mint
        uint256 finalSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Verify balance
        assertEq(finalSuperUSDCBalance, initialSuperUSDCBalance + mintAmount, "SuperUSDC balance should increase by mint amount");
        
        vm.stopPrank();
    }
    
    function testCrosschainBurn() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDC
        uint256 burnAmount = 500 * 10**6; // 500 SuperUSDC
        
        // First mint some tokens
        vm.prank(aiAgent);
        superUSDC.crosschainMint(user1, mintAmount);
        
        // Only aiAgent should be able to crosschain burn
        vm.startPrank(aiAgent);
        
        // Check balance before burn
        uint256 initialSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Perform crosschain burn
        superUSDC.crosschainBurn(user1, burnAmount);
        
        // Check balance after burn
        uint256 finalSuperUSDCBalance = superUSDC.balanceOf(user1);
        
        // Verify balance
        assertEq(finalSuperUSDCBalance, initialSuperUSDCBalance - burnAmount, "SuperUSDC balance should decrease by burn amount");
        
        vm.stopPrank();
    }
    
    function testUnauthorizedCrosschainMint() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDC
        
        // Try to mint from non-aiAgent address (should fail)
        vm.startPrank(user2);
        
        vm.expectRevert("Unauthorized: Only AI agent can mint");
        superUSDC.crosschainMint(user1, mintAmount);
        
        vm.stopPrank();
    }
    
    function testUnauthorizedCrosschainBurn() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDC
        uint256 burnAmount = 500 * 10**6; // 500 SuperUSDC
        
        // First mint some tokens
        vm.prank(aiAgent);
        superUSDC.crosschainMint(user1, mintAmount);
        
        // Try to burn from non-aiAgent address (should fail)
        vm.startPrank(user2);
        
        vm.expectRevert("Unauthorized: Only AI agent can burn");
        superUSDC.crosschainBurn(user1, burnAmount);
        
        vm.stopPrank();
    }
    
    function testInsufficientBalanceForBurn() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDC
        uint256 burnAmount = 2000 * 10**6; // 2,000 SuperUSDC (more than minted)
        
        // First mint some tokens
        vm.prank(aiAgent);
        superUSDC.crosschainMint(user1, mintAmount);
        
        // Try to burn more than balance (should fail)
        vm.startPrank(aiAgent);
        
        vm.expectRevert("Insufficient balance");
        superUSDC.crosschainBurn(user1, burnAmount);
        
        vm.stopPrank();
    }
    
    function testZeroAmountDeposit() public {
        // Try to deposit zero amount (should fail)
        vm.startPrank(user1);
        
        vm.expectRevert("Amount must be greater than zero");
        superUSDC.deposit(0);
        
        vm.stopPrank();
    }
    
    function testZeroAmountWithdrawal() public {
        // Try to withdraw zero amount (should fail)
        vm.startPrank(user1);
        
        vm.expectRevert("Amount must be greater than zero");
        superUSDC.withdraw(0);
        
        vm.stopPrank();
    }
    
    function testInsufficientFundsForWithdrawal() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDC
        uint256 withdrawAmount = 2000 * 10**6; // 2,000 USDC (more than deposited)
        
        // First deposit
        vm.prank(user1);
        superUSDC.deposit(depositAmount);
        
        // Try to withdraw more than balance (should fail)
        vm.startPrank(user1);
        
        vm.expectRevert("Insufficient sUSDC balance");
        superUSDC.withdraw(withdrawAmount);
        
        vm.stopPrank();
    }
} 