// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../lib/forge-std/src/Test.sol";
import "../contracts/interopusdt.sol";
import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

// Mock USDT token for testing
contract MockUSDT is ERC20 {
    constructor() ERC20("Tether USD", "USDT") {
        _mint(msg.sender, 1000000 * 10**6); // Mint 1M USDT to deployer
    }

    function decimals() public pure override returns (uint8) {
        return 6; // USDT has 6 decimals
    }
}

contract SuperUSDTTest is Test {
    SuperUSDT public superUSDT;
    MockUSDT public usdt;
    
    address public aiAgent;
    address public owner;
    address public user1;
    address public user2;
    
    uint256 public constant INITIAL_BALANCE = 10000 * 10**6; // 10,000 USDT (with 6 decimals)
    
    function setUp() public {
        // Set up accounts
        aiAgent = makeAddr("aiAgent");
        owner = makeAddr("owner");
        user1 = makeAddr("user1");
        user2 = makeAddr("user2");
        
        // Deploy mock USDT
        usdt = new MockUSDT();
        
        // Deploy SuperUSDT contract
        superUSDT = new SuperUSDT(aiAgent, owner, address(usdt));
        
        // Fund user accounts
        usdt.transfer(user1, INITIAL_BALANCE);
        usdt.transfer(user2, INITIAL_BALANCE);
        
        // Approve SuperUSDT to spend user's USDT
        vm.startPrank(user1);
        usdt.approve(address(superUSDT), type(uint256).max);
        vm.stopPrank();
        
        vm.startPrank(user2);
        usdt.approve(address(superUSDT), type(uint256).max);
        vm.stopPrank();
    }
    
    function testDeposit() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDT
        
        vm.startPrank(user1);
        
        // Check balances before deposit
        uint256 initialUSDTBalance = usdt.balanceOf(user1);
        uint256 initialSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Perform deposit
        superUSDT.deposit(depositAmount);
        
        // Check balances after deposit
        uint256 finalUSDTBalance = usdt.balanceOf(user1);
        uint256 finalSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Verify balances
        assertEq(finalUSDTBalance, initialUSDTBalance - depositAmount, "USDT balance should decrease by deposit amount");
        assertEq(finalSuperUSDTBalance, initialSuperUSDTBalance + depositAmount, "SuperUSDT balance should increase by deposit amount");
        
        vm.stopPrank();
    }
    
    function testWithdraw() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDT
        uint256 withdrawAmount = 500 * 10**6; // 500 USDT
        
        // First deposit
        vm.prank(user1);
        superUSDT.deposit(depositAmount);
        
        vm.startPrank(user1);
        
        // Check balances before withdrawal
        uint256 initialUSDTBalance = usdt.balanceOf(user1);
        uint256 initialSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Perform withdrawal
        superUSDT.withdraw(withdrawAmount);
        
        // Check balances after withdrawal
        uint256 finalUSDTBalance = usdt.balanceOf(user1);
        uint256 finalSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Verify balances
        assertEq(finalUSDTBalance, initialUSDTBalance + withdrawAmount, "USDT balance should increase by withdrawal amount");
        assertEq(finalSuperUSDTBalance, initialSuperUSDTBalance - withdrawAmount, "SuperUSDT balance should decrease by withdrawal amount");
        
        vm.stopPrank();
    }
    
    function testCrosschainMint() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDT
        
        // Only aiAgent should be able to crosschain mint
        vm.startPrank(aiAgent);
        
        // Check balance before mint
        uint256 initialSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Perform crosschain mint
        superUSDT.crosschainMint(user1, mintAmount);
        
        // Check balance after mint
        uint256 finalSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Verify balance
        assertEq(finalSuperUSDTBalance, initialSuperUSDTBalance + mintAmount, "SuperUSDT balance should increase by mint amount");
        
        vm.stopPrank();
    }
    
    function testCrosschainBurn() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDT
        uint256 burnAmount = 500 * 10**6; // 500 SuperUSDT
        
        // First mint some tokens
        vm.prank(aiAgent);
        superUSDT.crosschainMint(user1, mintAmount);
        
        // Only aiAgent should be able to crosschain burn
        vm.startPrank(aiAgent);
        
        // Check balance before burn
        uint256 initialSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Perform crosschain burn
        superUSDT.crosschainBurn(user1, burnAmount);
        
        // Check balance after burn
        uint256 finalSuperUSDTBalance = superUSDT.balanceOf(user1);
        
        // Verify balance
        assertEq(finalSuperUSDTBalance, initialSuperUSDTBalance - burnAmount, "SuperUSDT balance should decrease by burn amount");
        
        vm.stopPrank();
    }
    
    function testUnauthorizedCrosschainMint() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDT
        
        // Try to mint from non-aiAgent address (should fail)
        vm.startPrank(user2);
        
        vm.expectRevert("Unauthorized: Only AI agent can mint");
        superUSDT.crosschainMint(user1, mintAmount);
        
        vm.stopPrank();
    }
    
    function testUnauthorizedCrosschainBurn() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDT
        uint256 burnAmount = 500 * 10**6; // 500 SuperUSDT
        
        // First mint some tokens
        vm.prank(aiAgent);
        superUSDT.crosschainMint(user1, mintAmount);
        
        // Try to burn from non-aiAgent address (should fail)
        vm.startPrank(user2);
        
        vm.expectRevert("Unauthorized: Only AI agent can burn");
        superUSDT.crosschainBurn(user1, burnAmount);
        
        vm.stopPrank();
    }
    
    function testInsufficientBalanceForBurn() public {
        uint256 mintAmount = 1000 * 10**6; // 1,000 SuperUSDT
        uint256 burnAmount = 2000 * 10**6; // 2,000 SuperUSDT (more than minted)
        
        // First mint some tokens
        vm.prank(aiAgent);
        superUSDT.crosschainMint(user1, mintAmount);
        
        // Try to burn more than balance (should fail)
        vm.startPrank(aiAgent);
        
        vm.expectRevert("Insufficient balance");
        superUSDT.crosschainBurn(user1, burnAmount);
        
        vm.stopPrank();
    }
    
    function testZeroAmountDeposit() public {
        // Try to deposit zero amount (should fail)
        vm.startPrank(user1);
        
        vm.expectRevert("Amount must be greater than zero");
        superUSDT.deposit(0);
        
        vm.stopPrank();
    }
    
    function testZeroAmountWithdrawal() public {
        // Try to withdraw zero amount (should fail)
        vm.startPrank(user1);
        
        vm.expectRevert("Amount must be greater than zero");
        superUSDT.withdraw(0);
        
        vm.stopPrank();
    }
    
    function testInsufficientFundsForWithdrawal() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDT
        uint256 withdrawAmount = 2000 * 10**6; // 2,000 USDT (more than deposited)
        
        // First deposit
        vm.prank(user1);
        superUSDT.deposit(depositAmount);
        
        // Try to withdraw more than balance (should fail)
        vm.startPrank(user1);
        
        vm.expectRevert("Insufficient sUSDT balance");
        superUSDT.withdraw(withdrawAmount);
        
        vm.stopPrank();
    }
    
    function testEvents() public {
        uint256 depositAmount = 1000 * 10**6; // 1,000 USDT
        uint256 mintAmount = 500 * 10**6; // 500 USDT
        uint256 burnAmount = 200 * 10**6; // 200 USDT
        
        // Test Deposit event
        vm.startPrank(user1);
        vm.expectEmit(true, false, false, true);
        emit Deposited(user1, depositAmount);
        superUSDT.deposit(depositAmount);
        vm.stopPrank();
        
        // Test CrosschainMint event
        vm.startPrank(aiAgent);
        vm.expectEmit(true, false, false, true);
        emit CrosschainMinted(user2, mintAmount);
        superUSDT.crosschainMint(user2, mintAmount);
        vm.stopPrank();
        
        // Test CrosschainBurn event
        vm.startPrank(aiAgent);
        vm.expectEmit(true, false, false, true);
        emit CrosschainBurned(user2, burnAmount);
        superUSDT.crosschainBurn(user2, burnAmount);
        vm.stopPrank();
    }
} 