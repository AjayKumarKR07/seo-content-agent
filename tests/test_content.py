"""
Tests for SEO content generation
"""

import pytest
from agent.content_generator import ContentGenerator, ContentValidator
from agent.keyword_research import KeywordResearcher
from agent.seo_analyzer import SEOAnalyzer


class TestContentGenerator:
    """Test content generation"""
    
    def setup_method(self):
        """Setup for each test"""
        self.generator = ContentGenerator()
    
    def test_generate_blog_post(self):
        """Test blog post generation"""
        content = self.generator.generate(
            topic="Python Programming",
            content_type="blog_post",
            keywords=["python", "programming", "tutorial"]
        )
        
        assert content["title"] is not None
        assert content["content_type"] == "blog_post"
        assert len(content["keywords"]) == 3
    
    def test_generate_landing_page(self):
        """Test landing page generation"""
        content = self.generator.generate(
            topic="Web Development",
            content_type="landing_page",
            keywords=["web development"]
        )
        
        assert content["title"] is not None
        assert content["content_type"] == "landing_page"
    
    def test_invalid_content_type(self):
        """Test invalid content type"""
        with pytest.raises(ValueError):
            self.generator.generate(
                topic="Test",
                content_type="invalid_type",
                keywords=[]
            )
    
    def test_content_validation(self):
        """Test content validation"""
        content = {
            "title": "Test",
            "meta_description": "Test description",
            "body": "Test body",
            "keywords": []
        }
        
        assert ContentValidator.validate(content)
    
    def test_invalid_content_validation(self):
        """Test invalid content validation"""
        content = {"title": "Test"}
        
        assert not ContentValidator.validate(content)


class TestKeywordResearcher:
    """Test keyword research"""
    
    def setup_method(self):
        """Setup for each test"""
        self.researcher = KeywordResearcher()
    
    def test_research_keywords(self):
        """Test keyword research"""
        keywords = self.researcher.research("web development", limit=5)
        
        assert keywords is not None
        assert len(keywords) <= 5
    
    def test_keyword_metrics(self):
        """Test keyword metrics"""
        metrics = self.researcher.get_keyword_metrics("python")
        
        assert "search_volume" in metrics
        assert "difficulty_score" in metrics
        assert "cpc" in metrics
    
    def test_related_keywords(self):
        """Test related keywords"""
        related = self.researcher.get_related_keywords("SEO")
        
        assert len(related) > 0
        assert all("SEO" in keyword for keyword in related)


class TestSEOAnalyzer:
    """Test SEO analysis"""
    
    def setup_method(self):
        """Setup for each test"""
        self.analyzer = SEOAnalyzer()
    
    def test_analyze_content(self):
        """Test content analysis"""
        content = {
            "title": "Complete Guide to Python Programming",
            "meta_description": "Learn Python programming from basics to advanced topics",
            "body": "Python is a powerful programming language..." * 50,  # Long content
            "keywords": ["python", "programming"]
        }
        
        analysis = self.analyzer.analyze(content)
        
        assert "score" in analysis
        assert analysis["score"] >= 0
        assert analysis["score"] <= 100
    
    def test_short_content_penalty(self):
        """Test penalty for short content"""
        content = {
            "title": "Title",
            "meta_description": "Short description",
            "body": "Short content",
            "keywords": []
        }
        
        analysis = self.analyzer.analyze(content)
        
        assert analysis["content_analysis"]["issues"]


if __name__ == "__main__":
    pytest.main([__file__])
