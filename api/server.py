"""
FastAPI server for SEO Content Agent
"""

import logging
import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from agent.main import SEOContentAgent
from masumi_integration.payment_client import MasumiPaymentClient
from masumi_integration.identity_manager import IdentityManager
from masumi_integration.webhook_handler import WebhookHandler
from api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentRequest(BaseModel):
    """Request model for content generation"""
    topic: str
    content_type: str = "blog_post"
    target_keywords: Optional[List[str]] = None
    agent_id: Optional[str] = None


class PaymentRequest(BaseModel):
    """Request model for payment"""
    amount: float
    description: str
    agent_id: str


class WebhookRequest(BaseModel):
    """Request model for webhooks"""
    event_type: str
    transaction_id: str
    agent_id: str
    amount: Optional[float] = None


# Initialize FastAPI app
app = FastAPI(
    title="SEO Content Agent API",
    description="API for SEO content generation with Masumi payment integration",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
seo_agent = SEOContentAgent()
payment_client = MasumiPaymentClient()
identity_manager = IdentityManager()
webhook_handler = WebhookHandler(webhook_secret=os.getenv("WEBHOOK_SECRET"))

# Include routes
app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SEO Content Agent API",
        "version": "0.1.0"
    }


@app.get("/info")
async def get_info():
    """Get API information"""
    return {
        "name": "SEO Content Agent",
        "version": "0.1.0",
        "endpoints": [
            "/api/content/generate",
            "/api/payments/create",
            "/api/payments/confirm",
            "/api/agents/register",
            "/api/webhooks/payment"
        ]
    }


@app.post("/api/content/generate")
async def generate_content(request: ContentRequest, authorization: Optional[str] = Header(None)):
    """
    Generate SEO-optimized content
    
    Args:
        request: Content generation request
        authorization: Bearer token
        
    Returns:
        dict: Generated content
    """
    logger.info(f"Generating content for topic: {request.topic}")
    
    try:
        content = seo_agent.generate_seo_content(
            topic=request.topic,
            content_type=request.content_type,
            target_keywords=request.target_keywords
        )
        
        return {
            "status": "success",
            "content": content
        }
    except Exception as e:
        logger.error(f"Content generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/payments/create")
async def create_payment(request: PaymentRequest):
    """
    Create payment transaction
    
    Args:
        request: Payment request
        
    Returns:
        dict: Payment details
    """
    logger.info(f"Creating payment: ${request.amount} for agent {request.agent_id}")
    
    try:
        payment = payment_client.create_payment(
            amount=request.amount,
            description=request.description,
            agent_id=request.agent_id
        )
        
        return {
            "status": "success",
            "payment": payment
        }
    except Exception as e:
        logger.error(f"Payment creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/payments/confirm")
async def confirm_payment(transaction_id: str, payment_hash: str):
    """
    Confirm payment transaction
    
    Args:
        transaction_id: Transaction ID
        payment_hash: Payment proof hash
        
    Returns:
        dict: Confirmation result
    """
    logger.info(f"Confirming payment: {transaction_id}")
    
    try:
        result = payment_client.confirm_payment(
            transaction_id=transaction_id,
            payment_proof={"hash": payment_hash}
        )
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        logger.error(f"Payment confirmation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agents/register")
async def register_agent(agent_name: str):
    """
    Register new agent identity
    
    Args:
        agent_name: Name for the agent
        
    Returns:
        dict: Registration result
    """
    logger.info(f"Registering agent: {agent_name}")
    
    try:
        identity = identity_manager.create_identity(agent_name)
        
        registration = identity.register_with_masumi(
            api_key=os.getenv("MASUMI_API_KEY", "")
        )
        
        return {
            "status": "success",
            "registration": registration
        }
    except Exception as e:
        logger.error(f"Agent registration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/webhooks/payment")
async def handle_payment_webhook(request: WebhookRequest, x_signature: Optional[str] = Header(None)):
    """
    Handle payment webhook from Masumi
    
    Args:
        request: Webhook payload
        x_signature: Webhook signature
        
    Returns:
        dict: Processing result
    """
    logger.info(f"Received webhook: {request.event_type}")
    
    try:
        payload = request.dict()
        signature = x_signature or ""
        
        result = webhook_handler.process_webhook(payload, signature)
        
        return {
            "status": "processed",
            "result": result
        }
    except Exception as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/{agent_id}")
async def get_agent_info(agent_id: str):
    """
    Get agent information
    
    Args:
        agent_id: Agent ID
        
    Returns:
        dict: Agent information
    """
    identity = identity_manager.get_identity(agent_id)
    
    if not identity:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "status": "success",
        "agent": identity.export_identity()
    }


@app.get("/api/agents")
async def list_agents():
    """
    List all registered agents
    
    Returns:
        dict: All agents
    """
    agents = identity_manager.list_identities()
    
    return {
        "status": "success",
        "count": len(agents),
        "agents": agents
    }


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the API server
    
    Args:
        host: Server host
        port: Server port
    """
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    run_server(
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000))
    )
