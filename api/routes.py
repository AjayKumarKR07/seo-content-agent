"""
API routes for SEO Content Agent
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import logging

router = APIRouter(prefix="/api", tags=["api"])

logger = logging.getLogger(__name__)


@router.get("/keyword-research")
async def keyword_research(
    topic: str,
    limit: int = Query(5, ge=1, le=20)
):
    """
    Research keywords for a topic
    
    Args:
        topic: Topic to research
        limit: Number of keywords to return
        
    Returns:
        dict: Keywords and metrics
    """
    from agent.keyword_research import KeywordResearcher
    
    logger.info(f"Researching keywords for: {topic}")
    
    try:
        researcher = KeywordResearcher()
        keywords = researcher.research(topic, limit=limit)
        
        metrics = []
        for keyword in keywords:
            metric = researcher.get_keyword_metrics(keyword)
            metrics.append(metric)
        
        return {
            "status": "success",
            "topic": topic,
            "keywords": keywords,
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Keyword research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/seo-analysis")
async def seo_analysis(
    title: str,
    description: str,
    body: str
):
    """
    Analyze content for SEO
    
    Args:
        title: Content title
        description: Meta description
        body: Content body
        
    Returns:
        dict: SEO analysis results
    """
    from agent.seo_analyzer import SEOAnalyzer, OnPageOptimizer
    
    logger.info("Running SEO analysis")
    
    try:
        analyzer = SEOAnalyzer()
        
        content = {
            "title": title,
            "meta_description": description,
            "body": body,
            "keywords": []
        }
        
        analysis = analyzer.analyze(content)
        recommendations = OnPageOptimizer.get_recommendations(analysis)
        
        return {
            "status": "success",
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"SEO analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/content-templates")
async def get_content_templates():
    """
    Get available content templates
    
    Returns:
        dict: Available templates
    """
    from agent.content_generator import ContentGenerator
    
    try:
        generator = ContentGenerator()
        templates = generator.templates
        
        return {
            "status": "success",
            "count": len(templates),
            "templates": list(templates.keys()),
            "details": templates
        }
    except Exception as e:
        logger.error(f"Failed to get templates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/payment-status/{transaction_id}")
async def get_payment_status(transaction_id: str):
    """
    Get payment status
    
    Args:
        transaction_id: Transaction ID
        
    Returns:
        dict: Payment details
    """
    from masumi_integration.payment_client import MasumiPaymentClient
    
    logger.info(f"Getting payment status: {transaction_id}")
    
    try:
        client = MasumiPaymentClient()
        status = client.get_payment_status(transaction_id)
        
        return {
            "status": "success",
            "payment_status": status
        }
    except Exception as e:
        logger.error(f"Failed to get payment status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-webhook")
async def test_webhook(
    event_type: str = "payment.confirmed",
    amount: float = 5.00,
    agent_id: str = "test-agent"
):
    """
    Test webhook processing
    
    Args:
        event_type: Type of event
        amount: Payment amount
        agent_id: Agent ID
        
    Returns:
        dict: Processing result
    """
    from masumi_integration.webhook_handler import WebhookHandler
    
    logger.info(f"Testing webhook: {event_type}")
    
    try:
        handler = WebhookHandler()
        
        payload = {
            "id": "test-event-001",
            "event_type": event_type,
            "transaction_id": "TXN-TESTABCD1234",
            "agent_id": agent_id,
            "amount": amount
        }
        
        result = handler.process_webhook(payload, "")
        
        return {
            "status": "success",
            "webhook_result": result
        }
    except Exception as e:
        logger.error(f"Webhook test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
