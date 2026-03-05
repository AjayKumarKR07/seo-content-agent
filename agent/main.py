"""
Entry point for the SEO Content Agent
"""

import logging
from agent.content_generator import ContentGenerator
from agent.keyword_research import KeywordResearcher
from agent.seo_analyzer import SEOAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SEOContentAgent:
    """Main agent orchestrating SEO content creation"""
    
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.keyword_researcher = KeywordResearcher()
        self.seo_analyzer = SEOAnalyzer()
    
    def generate_seo_content(self, topic: str, content_type: str = "blog_post", target_keywords: list = None):
        """
        Generate SEO-optimized content
        
        Args:
            topic: Main topic for content
            content_type: Type of content (blog_post, landing_page)
            target_keywords: List of target keywords
            
        Returns:
            dict: Generated content with SEO metadata
        """
        logger.info(f"Generating {content_type} content for topic: {topic}")
        
        # Research keywords if not provided
        if not target_keywords:
            target_keywords = self.keyword_researcher.research(topic)
            logger.info(f"Researched keywords: {target_keywords}")
        
        # Generate content
        content = self.content_generator.generate(
            topic=topic,
            content_type=content_type,
            keywords=target_keywords
        )
        
        # Analyze and optimize
        seo_analysis = self.seo_analyzer.analyze(content)
        content['seo_analysis'] = seo_analysis
        
        logger.info(f"Content generated with SEO score: {seo_analysis.get('score', 'N/A')}")
        
        return content


def main():
    """Main entry point"""
    agent = SEOContentAgent()
    
    # Example usage
    content = agent.generate_seo_content(
        topic="Sustainable Web Hosting",
        content_type="blog_post",
        target_keywords=["sustainable hosting", "green web hosting", "eco-friendly servers"]
    )
    
    print(f"Generated Content: {content}")


if __name__ == "__main__":
    main()
