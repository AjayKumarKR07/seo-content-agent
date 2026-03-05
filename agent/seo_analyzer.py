"""
SEO optimization and analysis tools
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class SEOAnalyzer:
    """Analyzes content for SEO optimization"""
    
    def __init__(self):
        self.min_title_length = 30
        self.max_title_length = 60
        self.min_meta_length = 120
        self.max_meta_length = 160
        self.min_content_length = 300
    
    def analyze(self, content: Dict) -> Dict:
        """
        Analyze content for SEO factors
        
        Args:
            content: Content dictionary to analyze
            
        Returns:
            dict: SEO analysis results with score
        """
        logger.info("Starting SEO analysis")
        
        analysis = {
            "title_analysis": self._analyze_title(content.get("title", "")),
            "meta_analysis": self._analyze_meta(content.get("meta_description", "")),
            "content_analysis": self._analyze_content_body(content.get("body", "")),
            "keyword_analysis": self._analyze_keywords(content),
            "readability_score": self._calculate_readability(content.get("body", "")),
        }
        
        # Calculate overall score
        analysis["score"] = self._calculate_overall_score(analysis)
        
        return analysis
    
    def _analyze_title(self, title: str) -> Dict:
        """Analyze title tag"""
        issues = []
        
        if len(title) < self.min_title_length:
            issues.append(f"Title too short (< {self.min_title_length} chars)")
        elif len(title) > self.max_title_length:
            issues.append(f"Title too long (> {self.max_title_length} chars)")
        
        return {
            "length": len(title),
            "issues": issues,
            "status": "good" if not issues else "warning"
        }
    
    def _analyze_meta(self, meta: str) -> Dict:
        """Analyze meta description"""
        issues = []
        
        if len(meta) < self.min_meta_length:
            issues.append(f"Meta description too short (< {self.min_meta_length} chars)")
        elif len(meta) > self.max_meta_length:
            issues.append(f"Meta description too long (> {self.max_meta_length} chars)")
        
        return {
            "length": len(meta),
            "issues": issues,
            "status": "good" if not issues else "warning"
        }
    
    def _analyze_content_body(self, body: str) -> Dict:
        """Analyze content body"""
        issues = []
        word_count = len(body.split())
        
        if word_count < self.min_content_length:
            issues.append(f"Content too short (< {self.min_content_length} words)")
        
        return {
            "word_count": word_count,
            "issues": issues,
            "status": "good" if not issues else "warning"
        }
    
    def _analyze_keywords(self, content: Dict) -> Dict:
        """Analyze keyword optimization"""
        from agent.keyword_research import KeywordOptimizer
        
        keywords = content.get("keywords", [])
        body = content.get("body", "")
        
        keyword_analysis = {}
        for keyword in keywords:
            density = KeywordOptimizer.calculate_density(body, keyword)
            keyword_analysis[keyword] = {
                "density": density,
                "status": "optimal" if 1 <= density <= 3 else "needs_adjustment"
            }
        
        return keyword_analysis
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate content readability score (0-100)"""
        if not text:
            return 0.0
        
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        
        if sentences == 0:
            return 0.0
        
        # Simple readability metric
        avg_sentence_length = words / sentences
        
        # Scoring: 15-20 words per sentence is optimal
        if 15 <= avg_sentence_length <= 20:
            score = 90
        elif 10 <= avg_sentence_length <= 25:
            score = 75
        else:
            score = 50
        
        return min(100, max(0, score))
    
    def _calculate_overall_score(self, analysis: Dict) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 100
        
        # Deduct points for issues
        if analysis["title_analysis"]["issues"]:
            score -= 10
        
        if analysis["meta_analysis"]["issues"]:
            score -= 10
        
        if analysis["content_analysis"]["issues"]:
            score -= 15
        
        # Readability factor
        readability = analysis["readability_score"]
        if readability < 70:
            score -= 15
        
        return max(0, min(100, score))


class OnPageOptimizer:
    """Provides on-page optimization recommendations"""
    
    @staticmethod
    def get_recommendations(analysis: Dict) -> List[str]:
        """
        Get SEO recommendations based on analysis
        
        Args:
            analysis: SEO analysis results
            
        Returns:
            list: Optimization recommendations
        """
        recommendations = []
        
        if analysis["title_analysis"]["issues"]:
            recommendations.append("Optimize title tag length (30-60 characters)")
        
        if analysis["meta_analysis"]["issues"]:
            recommendations.append("Improve meta description (120-160 characters)")
        
        if analysis["content_analysis"]["issues"]:
            recommendations.append("Expand content to at least 300 words")
        
        if analysis["readability_score"] < 70:
            recommendations.append("Improve readability with shorter sentences")
        
        return recommendations
