import { ethers } from 'ethers';

// Contract ABIs
const SuperUSDCABI = [
  "function deposit(uint256 amount) external",
  "function withdraw(uint256 amount) external",
  "function balanceOf(address account) view returns (uint256)",
  "function decimals() view returns (uint8)",
  "function symbol() view returns (string)",
  "function name() view returns (string)",
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)"
];

// Contract addresses - replace with actual deployed addresses
const contractAddresses = {
  // Base Sepolia
  '84532': {
    SuperUSDC: '0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43',
    USDC: '0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238' // Mock USDC on Base Sepolia
  },
  // Optimism Sepolia
  '11155420': {
    SuperUSDC: '0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43',
    USDC: '0x8067F3Cb6eef936256806ED38B776C114BB0D9Db' // Mock USDC on Optimism Sepolia
  },
  // Zora Testnet
  '999': {
    SuperUSDC: '0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43',
    USDC: '0x4B83486DD8c2D2BAc812DDD37e6140b1D736ac8D' // Mock USDC on Zora
  },
  // Unichain Testnet
  '80002': {
    SuperUSDC: '0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43',
    USDC: '0x9b2690525572Ce621C378d37A3497Da4bDc746Fb' // Mock USDC on Unichain
  }
};

// Network information
const networks = {
  '84532': {
    name: 'Base Sepolia',
    explorer: 'https://sepolia.basescan.org',
    rpc: 'https://sepolia.base.org',
    chainId: '0x14913' // Hex format
  },
  '11155420': {
    name: 'Optimism Sepolia',
    explorer: 'https://sepolia-optimism.etherscan.io',
    rpc: 'https://sepolia.optimism.io',
    chainId: '0xA8F3C' // Hex format
  },
  '999': {
    name: 'Zora Testnet',
    explorer: 'https://testnet.explorer.zora.energy',
    rpc: 'https://testnet.rpc.zora.energy',
    chainId: '0x3E7' // Hex format
  },
  '80002': {
    name: 'Unichain Testnet',
    explorer: 'https://explorer.unichain.network',
    rpc: 'https://rpc.unichain.network',
    chainId: '0x13882' // Hex format
  }
};

class Web3Service {
  constructor() {
    this.provider = null;
    this.signer = null;
    this.contracts = {};
    this.currentChainId = null;
    this.userAddress = null;
  }

  // Connect to Web3 provider (MetaMask)
  async connect() {
    try {
      if (window.ethereum) {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        this.provider = new ethers.providers.Web3Provider(window.ethereum);
        this.signer = this.provider.getSigner();
        this.userAddress = await this.signer.getAddress();
        
        // Get current chain ID
        const network = await this.provider.getNetwork();
        this.currentChainId = network.chainId.toString();
        
        return {
          success: true,
          address: this.userAddress,
          chainId: this.currentChainId
        };
      } else {
        return {
          success: false,
          error: 'No Ethereum wallet found. Please install MetaMask.'
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Switch network
  async switchNetwork(targetChainId) {
    try {
      if (!this.provider) {
        throw new Error('Not connected to wallet');
      }

      const network = networks[targetChainId];
      
      if (!network) {
        throw new Error('Unsupported network');
      }

      try {
        // Try to switch to the network
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: network.chainId }],
        });
      } catch (switchError) {
        // If the network is not added, add it
        if (switchError.code === 4902) {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [
              {
                chainId: network.chainId,
                chainName: network.name,
                nativeCurrency: {
                  name: 'ETH',
                  symbol: 'ETH',
                  decimals: 18,
                },
                rpcUrls: [network.rpc],
                blockExplorerUrls: [network.explorer],
              },
            ],
          });
        } else {
          throw switchError;
        }
      }

      // Update current chain ID
      const updatedNetwork = await this.provider.getNetwork();
      this.currentChainId = updatedNetwork.chainId.toString();
      
      return {
        success: true,
        chainId: this.currentChainId
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Get SuperUSDC contract instance
  getContract(chainId = this.currentChainId) {
    if (!this.contracts[chainId]) {
      const addresses = contractAddresses[chainId];
      
      if (!addresses) {
        throw new Error(`Contract addresses not found for chain ID ${chainId}`);
      }
      
      this.contracts[chainId] = {
        SuperUSDC: new ethers.Contract(
          addresses.SuperUSDC,
          SuperUSDCABI,
          this.signer || this.provider
        ),
        USDC: new ethers.Contract(
          addresses.USDC,
          [
            "function balanceOf(address) view returns (uint256)",
            "function decimals() view returns (uint8)",
            "function symbol() view returns (string)",
            "function name() view returns (string)",
            "function approve(address, uint256) returns (bool)"
          ],
          this.signer || this.provider
        )
      };
    }
    
    return this.contracts[chainId];
  }

  // Get user balances
  async getBalances(chainId = this.currentChainId) {
    try {
      if (!this.userAddress) {
        throw new Error('Not connected to wallet');
      }
      
      const contracts = this.getContract(chainId);
      
      const superUSDCBalance = await contracts.SuperUSDC.balanceOf(this.userAddress);
      const usdcBalance = await contracts.USDC.balanceOf(this.userAddress);
      
      const superUSDCDecimals = await contracts.SuperUSDC.decimals();
      const usdcDecimals = await contracts.USDC.decimals();
      
      return {
        success: true,
        balances: {
          superUSDC: ethers.utils.formatUnits(superUSDCBalance, superUSDCDecimals),
          usdc: ethers.utils.formatUnits(usdcBalance, usdcDecimals)
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Approve USDC spending
  async approveUSDC(amount, chainId = this.currentChainId) {
    try {
      const contracts = this.getContract(chainId);
      const addresses = contractAddresses[chainId];
      
      const decimals = await contracts.USDC.decimals();
      const amountInWei = ethers.utils.parseUnits(amount.toString(), decimals);
      
      const tx = await contracts.USDC.approve(addresses.SuperUSDC, amountInWei);
      await tx.wait();
      
      return {
        success: true,
        txHash: tx.hash
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Check USDC allowance
  async checkAllowance(chainId = this.currentChainId) {
    try {
      if (!this.userAddress) {
        throw new Error('Not connected to wallet');
      }
      
      const contracts = this.getContract(chainId);
      const addresses = contractAddresses[chainId];
      
      const allowance = await contracts.USDC.allowance(
        this.userAddress,
        addresses.SuperUSDC
      );
      
      const decimals = await contracts.USDC.decimals();
      
      return {
        success: true,
        allowance: ethers.utils.formatUnits(allowance, decimals)
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Deposit USDC to get SuperUSDC
  async deposit(amount, chainId = this.currentChainId) {
    try {
      const contracts = this.getContract(chainId);
      
      const decimals = await contracts.USDC.decimals();
      const amountInWei = ethers.utils.parseUnits(amount.toString(), decimals);
      
      // Check allowance first
      const allowanceResponse = await this.checkAllowance(chainId);
      if (!allowanceResponse.success) {
        throw new Error('Failed to check allowance');
      }
      
      const allowanceInWei = ethers.utils.parseUnits(
        allowanceResponse.allowance,
        decimals
      );
      
      // If allowance is insufficient, approve first
      if (allowanceInWei.lt(amountInWei)) {
        const approveResponse = await this.approveUSDC(amount, chainId);
        if (!approveResponse.success) {
          throw new Error('Failed to approve USDC');
        }
      }
      
      // Perform deposit
      const tx = await contracts.SuperUSDC.deposit(amountInWei);
      await tx.wait();
      
      return {
        success: true,
        txHash: tx.hash
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Withdraw SuperUSDC to get USDC back
  async withdraw(amount, chainId = this.currentChainId) {
    try {
      const contracts = this.getContract(chainId);
      
      const decimals = await contracts.SuperUSDC.decimals();
      const amountInWei = ethers.utils.parseUnits(amount.toString(), decimals);
      
      const tx = await contracts.SuperUSDC.withdraw(amountInWei);
      await tx.wait();
      
      return {
        success: true,
        txHash: tx.hash
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Call the Skywire API to request cross-chain transfer
  async crossChainTransfer(amount, fromChainId, toChainId, recipient) {
    try {
      // Ensure we're on the source chain first
      if (this.currentChainId !== fromChainId) {
        const switchResponse = await this.switchNetwork(fromChainId);
        if (!switchResponse.success) {
          throw new Error('Failed to switch to source chain');
        }
      }
      
      // Get the signer's address if recipient is not provided
      recipient = recipient || this.userAddress;
      
      // Format API request
      const apiRequest = {
        instruction: `Transfer ${amount} SuperUSDC from ${networks[fromChainId].name} to ${networks[toChainId].name} for address ${recipient}`,
        chain_id: fromChainId,
        timeout: 120 // 2 minutes timeout
      };
      
      // Call the Skywire API
      const response = await fetch('http://localhost:8000/instruction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(apiRequest)
      });
      
      const data = await response.json();
      
      // Check if the request was accepted
      if (data.task_id) {
        return {
          success: true,
          taskId: data.task_id,
          status: data.status
        };
      } else {
        throw new Error('Failed to submit cross-chain transfer request');
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Check the status of a cross-chain transfer
  async checkTransferStatus(taskId) {
    try {
      const response = await fetch(`http://localhost:8000/task/${taskId}`);
      const data = await response.json();
      
      return {
        success: true,
        taskId: data.task_id,
        status: data.status,
        result: data.result,
        error: data.error
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// Create and export a singleton instance
const web3Service = new Web3Service();
export default web3Service; 