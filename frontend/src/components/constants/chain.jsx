// src/constants/chains.js
import optimism from '../../assets/optimism.svg';
import baseIcon from '../../assets/base.svg';

export const SUPERETH_ABI = [
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function decimals() view returns (uint8)",
  "function totalSupply() view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
  "function transfer(address to, uint256 amount) returns (bool)",
  "function deposit() payable",
  "function withdraw(uint256 amount)",
  "function crosschainMint(address to, uint256 amount)",
  "function crosschainBurn(address from, uint256 amount)",
  "event Deposited(address indexed user, uint256 amount)",
  "event Withdrawn(address indexed user, uint256 amount)",
  "event CrosschainMinted(address indexed receiver, uint256 amount)",
  "event CrosschainBurned(address indexed from, uint256 amount)"
];

export const CONTRACT_ADDRESS = "0x13D962B70e8E280c7762557Ef8Bf89Fdc93e3F43";

const ZoraLogo = () => (
  <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#000000"/>
    <path d="M6 8.5L12 5L18 8.5V15.5L12 19L6 15.5V8.5Z" fill="white"/>
  </svg>
);

const BaseLogo = () => (
  <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#0052FF"/>
    <path d="M12 6L16.5 8.75V14.25L12 17L7.5 14.25V8.75L12 6Z" fill="white"/>
  </svg>
);

export const SUPPORTED_CHAINS = [
  {
    chainName: "Optimism Sepolia",
    chainId: "0xA8F3C",
    chainIdDecimal: 690556,
    icon: <img src={optimism} alt="Optimism Icon" className="w-10 h-10 bg-transparent" />
  },
  {
    chainName: "Base Sepolia",
    chainId: "0x14913",
    chainIdDecimal: 84531,
    icon: <img src={baseIcon} alt="Base Icon" className="w-10 h-10 bg-transparent" />
  },
  {
    chainName: "Zora",
    chainId: "0x7777777",
    chainIdDecimal: 7777777,
    icon: <ZoraLogo className="w-10 h-10 bg-transparent" />
  },
  {
    chainName: "Unichain",
    chainId: "0x82",
    chainIdDecimal: 130,
    icon: <svg width="40" height="42" viewBox="0 0 116 115" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M115.476 56.406C84.3089 56.406 59.07 31.1416 59.07 0H56.8819V56.406H0.47583V58.594C31.6429 58.594 56.8819 83.8584 56.8819 115H59.07V58.594H115.476V56.406Z" fill="#06b6d4"/>
    </svg>
  },
];