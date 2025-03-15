// src/components/bridge/ActionSelector.jsx
import React from 'react';
import { ArrowLeftRight, Download, Upload } from 'lucide-react';
import { BridgeActionButton } from '../common/Inputs';

const ActionSelector = ({ activeAction, setActiveAction }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <BridgeActionButton
        onClick={() => setActiveAction('bridge')}
        icon={ArrowLeftRight}
        label="Bridge"
        description="Transfer across chains"
        active={activeAction === 'bridge'}
      />
      <BridgeActionButton
        onClick={() => setActiveAction('deposit')}
        icon={Download}
        label="Deposit"
        description="ETH to SuperETH"
        active={activeAction === 'deposit'}
      />
      <BridgeActionButton
        onClick={() => setActiveAction('withdraw')}
        icon={Upload}
        label="Withdraw"
        description="SuperETH to ETH"
        active={activeAction === 'withdraw'}
      />
    </div>
  );
};

export default ActionSelector;