"""
Tests for payment and Masumi integration
"""

import pytest
from masumi_integration.payment_client import MasumiPaymentClient, PaymentValidator
from masumi_integration.identity_manager import AgentIdentity, IdentityManager
from masumi_integration.webhook_handler import WebhookHandler


class TestPaymentClient:
    """Test Masumi payment client"""
    
    def setup_method(self):
        """Setup for each test"""
        self.client = MasumiPaymentClient()
    
    def test_create_payment(self):
        """Test payment creation"""
        payment = self.client.create_payment(
            amount=10.00,
            description="Test payment",
            agent_id="test-agent-001"
        )
        
        assert "transaction_id" in payment
        assert payment["amount"] == 10.00
        assert payment["status"] == "pending"
    
    def test_confirm_payment(self):
        """Test payment confirmation"""
        payment = self.client.create_payment(10.00, "Test", "test-agent")
        
        result = self.client.confirm_payment(
            transaction_id=payment["transaction_id"],
            payment_proof={"hash": "test_hash"}
        )
        
        assert result["status"] == "confirmed"
        assert "confirmation_hash" in result
    
    def test_get_payment_status(self):
        """Test getting payment status"""
        payment = self.client.create_payment(5.00, "Test", "test-agent")
        
        status = self.client.get_payment_status(payment["transaction_id"])
        
        assert status["status"] == "confirmed"
        assert status["amount"] == 5.00
    
    def test_refund_payment(self):
        """Test payment refund"""
        payment = self.client.create_payment(5.00, "Test", "test-agent")
        
        refund = self.client.refund_payment(
            transaction_id=payment["transaction_id"],
            reason="Testing"
        )
        
        assert refund["status"] == "refunded"
        assert "refund_id" in refund


class TestPaymentValidator:
    """Test payment validation"""
    
    def test_validate_amount(self):
        """Test amount validation"""
        assert PaymentValidator.validate_amount(10.00)
        assert PaymentValidator.validate_amount(1)
        assert not PaymentValidator.validate_amount(-5)
        assert not PaymentValidator.validate_amount(0)
    
    def test_validate_transaction_id(self):
        """Test transaction ID validation"""
        from masumi_integration.payment_client import MasumiPaymentClient
        
        txn_id = MasumiPaymentClient._generate_transaction_id()
        assert PaymentValidator.validate_transaction_id(txn_id)
    
    def test_validate_payment_proof(self):
        """Test payment proof validation"""
        valid_proof = {
            "hash": "abc123",
            "signature": "sig123",
            "timestamp": "2024-01-01"
        }
        
        assert PaymentValidator.validate_payment_proof(valid_proof)
        
        invalid_proof = {"hash": "abc123"}
        assert not PaymentValidator.validate_payment_proof(invalid_proof)


class TestAgentIdentity:
    """Test agent identity"""
    
    def test_create_identity(self):
        """Test identity creation"""
        identity = AgentIdentity(name="Test Agent")
        
        assert identity.agent_id is not None
        assert identity.name == "Test Agent"
    
    def test_register_with_masumi(self):
        """Test Masumi registration"""
        identity = AgentIdentity(name="Test Agent")
        
        result = identity.register_with_masumi("test_api_key")
        
        assert result["status"] == "registered"
        assert "wallet_address" in result
    
    def test_add_capability(self):
        """Test adding capability"""
        identity = AgentIdentity()
        
        identity.add_capability("content_generation")
        identity.add_capability("keyword_research")
        
        assert "content_generation" in identity.capabilities
        assert "keyword_research" in identity.capabilities
    
    def test_verify_identity(self):
        """Test identity verification"""
        identity = AgentIdentity()
        
        result = identity.verify_identity("signature", "message")
        
        assert result
    
    def test_export_identity(self):
        """Test identity export"""
        identity = AgentIdentity(name="Test")
        exported = identity.export_identity()
        
        assert "agent_id" in exported
        assert "name" in exported
        assert exported["name"] == "Test"


class TestIdentityManager:
    """Test identity manager"""
    
    def setup_method(self):
        """Setup for each test"""
        self.manager = IdentityManager()
    
    def test_create_identity(self):
        """Test creating identity"""
        identity = self.manager.create_identity("Agent 1")
        
        assert identity is not None
        assert identity.name == "Agent 1"
    
    def test_get_identity(self):
        """Test getting identity"""
        identity = self.manager.create_identity("Agent 2")
        
        retrieved = self.manager.get_identity(identity.agent_id)
        
        assert retrieved is not None
        assert retrieved.agent_id == identity.agent_id
    
    def test_list_identities(self):
        """Test listing identities"""
        self.manager.create_identity("Agent A")
        self.manager.create_identity("Agent B")
        
        identities = self.manager.list_identities()
        
        assert len(identities) >= 2


class TestWebhookHandler:
    """Test webhook handling"""
    
    def setup_method(self):
        """Setup for each test"""
        self.handler = WebhookHandler(webhook_secret="test_secret")
    
    def test_handle_payment_confirmed(self):
        """Test payment confirmed webhook"""
        event = {
            "id": "evt_001",
            "transaction_id": "TXN-ABC123",
            "amount": 5.00,
            "agent_id": "agent_001"
        }
        
        result = self.handler.handle_payment_confirmed(event)
        
        assert result["status"] == "processed"
        assert result["event_id"] == "evt_001"
    
    def test_handle_payment_failed(self):
        """Test payment failed webhook"""
        event = {
            "id": "evt_002",
            "transaction_id": "TXN-XYZ789",
            "error_message": "Insufficient funds"
        }
        
        result = self.handler.handle_payment_failed(event)
        
        assert result["status"] == "failed"
    
    def test_prevent_duplicate_events(self):
        """Test duplicate event prevention"""
        event = {
            "id": "evt_003",
            "transaction_id": "TXN-DUP123",
            "amount": 5.00,
            "agent_id": "agent_001"
        }
        
        # Process first time
        result1 = self.handler.handle_payment_confirmed(event)
        assert result1["status"] == "processed"
        
        # Process duplicate
        result2 = self.handler.handle_payment_confirmed(event)
        assert result2["status"] == "duplicate"


if __name__ == "__main__":
    pytest.main([__file__])
