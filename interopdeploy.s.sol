// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import { Script, console } from "../lib/forge-std/src/Script.sol";
import { SuperETH } from "../src/interop.sol";

contract DeploySuperETH is Script {
    function run() external {
        address aiAgent = 0x72a4d3cC389121c911B3A72BD4d495D3D640ad00; // Replace with AI agent address
        address owner = 0x72a4d3cC389121c911B3A72BD4d495D3D640ad00; // Replace with owner address

        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        bytes32 salt = keccak256(abi.encodePacked("SuperETH_Salt"));

        vm.startBroadcast(deployerPrivateKey);

        SuperETH superETH = new SuperETH{salt: salt}(aiAgent, owner);
        console.log("SuperETH deployed at:", address(superETH));

        vm.stopBroadcast();
    }
}