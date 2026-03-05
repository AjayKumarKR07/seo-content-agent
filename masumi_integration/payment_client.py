"""
Masumi payment client for handling transactions
"""

import os
import logging
from typing import Dict, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class MasumiPaymentClient:
    """Client for Masumi payment API integration"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("MASUMI_API_KEY")
        self.base_url = base_url or os.getenv("MASUMI_BASE_URL", "https://api.masumi.io")
        self.timeout = 30
        
        if not self.api_key:
            logger.warning("MASUMI_API_KEY not configured")
    
    def create_payment(self, amount: float, description: str, agent_id: str) -> Dict:
        """
        Create a payment transaction
        
        Args:
            amount: Payment amount in USD
            description: Payment description
            agent_id: ID of agent requesting payment
            
        Returns:
            dict: Payment transaction details
        """
        logger.info(f"Creating payment: ${amount} for agent {agent_id}")
        
        # Mock payment creation - would call actual Masumi API
        payment = {
            "transaction_id": self._generate_transaction_id(),
            "amount": amount,
            "currency": "USD",
            "description": description,
            "agent_id": agent_id,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": self._get_expiration_time()
        }
        
        return payment
    
    def confirm_payment(self, transaction_id: str, payment_proof: Dict) -> Dict:
        """
        Confirm a payment with proof
        
        Args:
            transaction_id: Transaction ID to confirm
            payment_proof: Proof of payment (signature, hash, etc.)
            
        Returns:
            dict: Confirmation result
        """
        logger.info(f"Confirming payment: {transaction_id}")
        
        result = {
            "transaction_id": transaction_id,
            "status": "confirmed",
            "confirmation_hash": payment_proof.get("hash", ""),
            "verified_at": datetime.utcnow().isoformat(),
            "blockchain_tx": self._get_mock_blockchain_tx()
        }
        
        return result
    
    def get_payment_status(self, transaction_id: str) -> Dict:
        """
        Get payment status
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            dict: Payment status details
        """
        logger.info(f"Checking payment status: {transaction_id}")
        
        return {
            "transaction_id": transaction_id,
            "status": "confirmed",
            "amount": 5.00,
            "currency": "USD",
            "confirmed_at": datetime.utcnow().isoformat()
        }
    
    def refund_payment(self, transaction_id: str, reason: str) -> Dict:
        """
        Refund a payment
        
        Args:
            transaction_id: Transaction ID to refund
            reason: Refund reason
            
        Returns:
            dict: Refund details
        """
        logger.info(f"Refunding payment: {transaction_id} - Reason: {reason}")
        
        return {
            "transaction_id": transaction_id,
            "refund_id": self._generate_transaction_id(),
            "status": "refunded",
            "amount": 5.00,
            "reason": reason,
            "refunded_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _generate_transaction_id() -> str:
        """Generate unique transaction ID"""
        from uuid import uuid4
        return f"TXN-{uuid4().hex[:12].upper()}"
    
    @staticmethod
    def _get_expiration_time() -> str:
        """Get payment expiration time (24 hours from now)"""
        from datetime import timedelta
        expiration = datetime.utcnow() + timedelta(hours=24)
        return expiration.isoformat()
    
    @staticmethod
    def _get_mock_blockchain_tx() -> str:
        """Get mock blockchain transaction hash"""
        import hashlib
        mock_data = f"{datetime.utcnow().isoformat()}".encode()
        return f"0x{hashlib.sha256(mock_data).hexdigest()}"


class PaymentValidator:
    """Validates payment information"""
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate payment amount"""
        return isinstance(amount, (int, float)) and amount > 0
    
    @staticmethod
    def validate_transaction_id(transaction_id: str) -> bool:
        """Validate transaction ID format"""
        return transaction_id.startswith("TXN-") and len(transaction_id) == 16
    
    @staticmethod
    def validate_payment_proof(proof: Dict) -> bool:
        """Validate payment proof"""
        required_fields = ["hash", "signature", "timestamp"]
        return all(field in proof for field in required_fields)
