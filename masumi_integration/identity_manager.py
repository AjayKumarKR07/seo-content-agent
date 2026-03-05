"""
Agent identity management for Masumi integration
"""

import os
import logging
from typing import Dict, Optional
from uuid import uuid4
import json

logger = logging.getLogger(__name__)


class AgentIdentity:
    """Manages agent identity and credentials"""
    
    def __init__(self, agent_id: Optional[str] = None, name: str = "SEO Content Agent"):
        self.agent_id = agent_id or str(uuid4())
        self.name = name
        self.created_at = None
        self.credentials = {}
        self.capabilities = []
        self.masumi_wallet = None
    
    def register_with_masumi(self, api_key: str) -> Dict:
        """
        Register agent identity with Masumi
        
        Args:
            api_key: Masumi API key
            
        Returns:
            dict: Registration result with wallet info
        """
        logger.info(f"Registering agent {self.agent_id} with Masumi")
        
        self.credentials["masumi_api_key"] = api_key
        self.credentials["registered"] = True
        
        # Generate Masumi wallet for this agent
        self.masumi_wallet = self._create_masumi_wallet()
        
        result = {
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "status": "registered",
            "wallet_address": self.masumi_wallet["address"],
            "capabilities": ["content_generation", "keyword_research", "seo_analysis"]
        }
        
        return result
    
    def get_masumi_wallet(self) -> Dict:
        """
        Get Masumi wallet information
        
        Returns:
            dict: Wallet details
        """
        if not self.masumi_wallet:
            self.masumi_wallet = self._create_masumi_wallet()
        
        return self.masumi_wallet
    
    def add_capability(self, capability: str) -> None:
        """
        Add capability to agent
        
        Args:
            capability: Capability name
        """
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            logger.info(f"Added capability: {capability}")
    
    def verify_identity(self, signature: str, message: str) -> bool:
        """
        Verify agent identity with signature
        
        Args:
            signature: Digital signature
            message: Message that was signed
            
        Returns:
            bool: Verification result
        """
        logger.info(f"Verifying identity for agent {self.agent_id}")
        
        # In real implementation, verify cryptographic signature
        # For now, mock verification
        return len(signature) > 0 and len(message) > 0
    
    def export_identity(self) -> Dict:
        """
        Export agent identity (excluding sensitive data)
        
        Returns:
            dict: Public identity information
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": self.capabilities,
            "wallet_address": self.masumi_wallet["address"] if self.masumi_wallet else None,
            "registered": self.credentials.get("registered", False)
        }
    
    @staticmethod
    def _create_masumi_wallet() -> Dict:
        """Create Masumi wallet for agent"""
        from uuid import uuid4
        import hashlib
        
        wallet_id = str(uuid4())
        address = f"masumi_{hashlib.sha256(wallet_id.encode()).hexdigest()[:20]}"
        
        return {
            "address": address,
            "balance": 0.0,
            "created_at": None,
            "transactions": []
        }


class IdentityManager:
    """Manages multiple agent identities"""
    
    def __init__(self):
        self.identities: Dict[str, AgentIdentity] = {}
        self.identity_file = os.getenv("IDENTITY_FILE", ".identities.json")
    
    def create_identity(self, name: str) -> AgentIdentity:
        """
        Create new agent identity
        
        Args:
            name: Agent name
            
        Returns:
            AgentIdentity: New identity
        """
        identity = AgentIdentity(name=name)
        self.identities[identity.agent_id] = identity
        logger.info(f"Created identity: {identity.agent_id}")
        
        return identity
    
    def get_identity(self, agent_id: str) -> Optional[AgentIdentity]:
        """
        Get identity by ID
        
        Args:
            agent_id: Agent ID
            
        Returns:
            AgentIdentity or None
        """
        return self.identities.get(agent_id)
    
    def list_identities(self) -> Dict[str, Dict]:
        """
        List all managed identities
        
        Returns:
            dict: All identities (public data only)
        """
        return {
            agent_id: identity.export_identity()
            for agent_id, identity in self.identities.items()
        }
    
    def save_identities(self) -> None:
        """Save identities to file"""
        identities_data = {
            agent_id: identity.export_identity()
            for agent_id, identity in self.identities.items()
        }
        
        with open(self.identity_file, 'w') as f:
            json.dump(identities_data, f, indent=2)
        
        logger.info(f"Saved {len(identities_data)} identities")
    
    def load_identities(self) -> None:
        """Load identities from file"""
        if not os.path.exists(self.identity_file):
            logger.info("No identity file found")
            return
        
        with open(self.identity_file, 'r') as f:
            identities_data = json.load(f)
        
        for agent_id, data in identities_data.items():
            identity = AgentIdentity(agent_id=agent_id, name=data.get("name"))
            identity.capabilities = data.get("capabilities", [])
            self.identities[agent_id] = identity
        
        logger.info(f"Loaded {len(identities_data)} identities")
