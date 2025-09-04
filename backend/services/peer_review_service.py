#!/usr/bin/env python3
"""
Peer Review Service for ArxivMind
"""

from typing import Dict, Any

class PeerReviewService:
    def __init__(self, rag_service=None):
        if rag_service:
            self.rag_service = rag_service
        else:
            # This should not happen if called properly
            import os
            from .rag_service import RAGService
            openrouter_key = os.getenv("OPENROUTER_KEY", "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")
            self.rag_service = RAGService(openrouter_key)

    async def generate_review(self, content: str, title: str, review_type: str) -> Dict[str, Any]:
        """Generate peer review based on paper content and review type"""
        
        # Customize prompt based on review type
        prompts = {
            "Standard Review": "Provide a comprehensive academic peer review of this paper. Include strengths, weaknesses, significance, and recommendations.",
            "Detailed Analysis": "Conduct a thorough analysis including methodology validation, result interpretation, and detailed feedback for improvement.",
            "Conference Review": "Review as if for a top-tier conference. Provide scores, technical assessment, and acceptance recommendation.",
            "Journal Review": "Provide a detailed journal-style review with major and minor revision points and publication recommendation.",
            "Technical Review": "Focus on technical soundness, implementation details, reproducibility, and methodological rigor.",
            "balanced": "Provide a fair and balanced academic review highlighting both strengths and areas for improvement.",
            "strict": "Conduct a rigorous critique focusing on potential weaknesses and areas needing significant improvement.",
            "constructive": "Provide helpful, constructive feedback aimed at improving the paper's quality and impact."
        }

        prompt = prompts.get(review_type, prompts["balanced"])
        
        # Generate review using RAG service with OpenRouter
        review_prompt = f"""
        Title: {title}
        
        Content: {content}
        
        Task: {prompt}
        
        Please structure your review with clear sections covering:
        1. Summary of the paper
        2. Strengths and contributions
        3. Weaknesses and limitations
        4. Specific comments and suggestions
        5. Overall recommendation
        """
        
        review = await self.rag_service.analyze(
            text=content,
            task=review_prompt
        )

        # Structure the response
        sections = {
            "Standard Review": ["Summary", "Strengths", "Weaknesses", "Recommendations"],
            "Detailed Analysis": ["Overview", "Methodology", "Results", "Discussion", "Improvements"],
            "Conference Review": ["Summary", "Technical Merit", "Novelty", "Impact", "Score"],
            "Journal Review": ["Summary", "Major Points", "Minor Points", "Recommendation"],
            "Technical Review": ["Technical Assessment", "Implementation", "Reproducibility", "Suggestions"],
            "balanced": ["Summary", "Strengths", "Areas for Improvement", "Recommendation"],
            "strict": ["Summary", "Critical Issues", "Major Concerns", "Required Changes"],
            "constructive": ["Summary", "Positive Aspects", "Suggestions", "Future Directions"]
        }

        return {
            "review_type": review_type,
            "sections": sections.get(review_type, sections["balanced"]),
            "content": review,
            "metadata": {
                "title": title,
                "timestamp": "2025-09-03T12:00:00",
                "version": "2.0.0"
            }
        }
