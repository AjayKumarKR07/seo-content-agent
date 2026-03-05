"""
Core SEO content generation logic
"""

import json
import os
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates SEO-optimized content from templates"""
    
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load content templates"""
        templates = {}
        for template_file in os.listdir(self.templates_dir):
            if template_file.endswith(".json"):
                template_name = template_file.replace(".json", "")
                with open(os.path.join(self.templates_dir, template_file), 'r') as f:
                    templates[template_name] = json.load(f)
        logger.info(f"Loaded {len(templates)} templates")
        return templates
    
    def generate(self, topic: str, content_type: str, keywords: List[str]) -> Dict:
        """
        Generate SEO content based on template
        
        Args:
            topic: Main topic
            content_type: Type of content (blog_post, landing_page)
            keywords: List of keywords to incorporate
            
        Returns:
            dict: Generated content
        """
        if content_type not in self.templates:
            raise ValueError(f"Unknown content type: {content_type}")
        
        template = self.templates[content_type]
        
        # Generate content from template
        content = {
            "title": self._generate_title(topic, template),
            "meta_description": self._generate_meta(topic, keywords, template),
            "headings": self._generate_headings(topic, keywords, template),
            "body": self._generate_body(topic, keywords, template),
            "keywords": keywords,
            "content_type": content_type,
            "template_used": template.get("name")
        }
        
        return content
    
    def _generate_title(self, topic: str, template: Dict) -> str:
        """Generate SEO title"""
        title_template = template.get("title_template", "{topic}")
        return title_template.format(topic=topic)
    
    def _generate_meta(self, topic: str, keywords: List[str], template: Dict) -> str:
        """Generate meta description"""
        key_phrase = keywords[0] if keywords else topic
        return f"Learn about {topic}. Expert guide on {key_phrase}. Comprehensive resource for SEO optimization."
    
    def _generate_headings(self, topic: str, keywords: List[str], template: Dict) -> List[str]:
        """Generate content headings"""
        headings = [
            f"Introduction to {topic}",
            f"Why {topic} Matters",
            f"Key Aspects of {topic}",
            f"How to Optimize {topic}",
            f"Conclusion"
        ]
        return headings
    
    def _generate_body(self, topic: str, keywords: List[str], template: Dict) -> str:
        """Generate body content"""
        body_template = template.get("body_template", "")
        body = f"""
        This comprehensive guide covers everything you need to know about {topic}.
        
        {topic} is a crucial aspect of modern digital strategy. By understanding and implementing
        best practices related to {', '.join(keywords[:2])}, you can significantly improve your results.
        
        Throughout this article, we'll explore the key concepts, strategies, and tools that can help
        you master {topic}. Whether you're a beginner or an experienced professional, you'll find
        valuable insights and actionable advice.
        """
        return body.strip()


class ContentValidator:
    """Validates generated content quality"""
    
    @staticmethod
    def validate(content: Dict) -> bool:
        """
        Validate generated content
        
        Args:
            content: Content dictionary to validate
            
        Returns:
            bool: Validation result
        """
        required_fields = ["title", "meta_description", "body", "keywords"]
        return all(field in content for field in required_fields)
