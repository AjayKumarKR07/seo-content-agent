"""
Webhook handler for Masumi payment confirmations
"""

import logging
import hashlib
import hmac
import json
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handles incoming Masumi payment webhooks"""
    
    def __init__(self, webhook_secret: Optional[str] = None):
        self.webhook_secret = webhook_secret
        self.processed_events = set()
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature
        
        Args:
            payload: Webhook payload
            signature: Provided signature
            
        Returns:
            bool: Signature valid
        """
        if not self.webhook_secret:
            logger.warning("Webhook secret not configured")
            return False
        
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    def handle_payment_confirmed(self, event: Dict) -> Dict:
        """
        Handle payment confirmed webhook event
        
        Args:
            event: Webhook event data
            
        Returns:
            dict: Handling result
        """
        event_id = event.get("id")
        
        # Prevent duplicate processing
        if event_id in self.processed_events:
            logger.warning(f"Duplicate event: {event_id}")
            return {"status": "duplicate", "event_id": event_id}
        
        logger.info(f"Processing payment confirmation: {event_id}")
        
        transaction_id = event.get("transaction_id")
        amount = event.get("amount")
        agent_id = event.get("agent_id")
        
        # Process payment confirmation
        result = {
            "status": "processed",
            "event_id": event_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "agent_id": agent_id,
            "processed_at": datetime.utcnow().isoformat()
        }
        
        self.processed_events.add(event_id)
        
        return result
    
    def handle_payment_failed(self, event: Dict) -> Dict:
        """
        Handle payment failed webhook event
        
        Args:
            event: Webhook event data
            
        Returns:
            dict: Handling result
        """
        event_id = event.get("id")
        
        logger.error(f"Payment failed: {event_id} - {event.get('error_message')}")
        
        result = {
            "status": "failed",
            "event_id": event_id,
            "transaction_id": event.get("transaction_id"),
            "reason": event.get("error_message"),
            "processed_at": datetime.utcnow().isoformat()
        }
        
        return result
    
    def handle_refund_completed(self, event: Dict) -> Dict:
        """
        Handle refund completed webhook event
        
        Args:
            event: Webhook event data
            
        Returns:
            dict: Handling result
        """
        event_id = event.get("id")
        
        logger.info(f"Processing refund: {event_id}")
        
        result = {
            "status": "refunded",
            "event_id": event_id,
            "transaction_id": event.get("transaction_id"),
            "refund_id": event.get("refund_id"),
            "amount": event.get("amount"),
            "processed_at": datetime.utcnow().isoformat()
        }
        
        return result
    
    def process_webhook(self, payload: Dict, signature: str) -> Dict:
        """
        Process incoming webhook
        
        Args:
            payload: Webhook payload
            signature: Webhook signature
            
        Returns:
            dict: Processing result
        """
        # Verify signature
        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        if not self.verify_webhook_signature(payload_str, signature):
            logger.error("Webhook signature verification failed")
            return {"status": "unauthorized", "error": "Invalid signature"}
        
        event_type = payload.get("event_type")
        
        # Route to appropriate handler
        handlers = {
            "payment.confirmed": self.handle_payment_confirmed,
            "payment.failed": self.handle_payment_failed,
            "refund.completed": self.handle_refund_completed
        }
        
        handler = handlers.get(event_type)
        if not handler:
            logger.warning(f"Unknown event type: {event_type}")
            return {"status": "unknown_event", "event_type": event_type}
        
        return handler(payload)


class WebhookEventLogger:
    """Logs webhook events for audit and debugging"""
    
    def __init__(self, log_file: str = "webhook_events.log"):
        self.log_file = log_file
    
    def log_event(self, event: Dict, result: Dict) -> None:
        """
        Log webhook event and result
        
        Args:
            event: Original event
            result: Processing result
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "result": result
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_events(self, agent_id: Optional[str] = None, limit: int = 100) -> list:
        """
        Retrieve logged events
        
        Args:
            agent_id: Optional filter by agent
            limit: Max events to return
            
        Returns:
            list: Events
        """
        events = []
        
        if not os.path.exists(self.log_file):
            return events
        
        with open(self.log_file, 'r') as f:
            for line in f.readlines()[-limit:]:
                try:
                    log_entry = json.loads(line)
                    if agent_id is None or log_entry.get("event", {}).get("agent_id") == agent_id:
                        events.append(log_entry)
                except json.JSONDecodeError:
                    continue
        
        return events


import os
