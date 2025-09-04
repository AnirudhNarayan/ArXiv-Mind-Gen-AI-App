#!/usr/bin/env python3
"""
OpenRouter LLM Analyzer Service
Advanced AI-powered analysis using multiple premium models with cost optimization
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class OpenRouterAnalyzer:
    """Service for AI-powered paper analysis using OpenRouter's multiple LLM providers"""
    
    def __init__(self):
        """Initialize with OpenRouter configuration and cost tracking"""
        self.openrouter_key = "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"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://arxivmind.com",
            "X-Title": "ArxivMind",
            "Content-Type": "application/json"
        }
        
        # Cost-optimized model selection (staying under $2 budget)
        self.models = {
            "search": "openai/gpt-4o-mini",  # $0.15/1M tokens - for search
            "summary": "anthropic/claude-3-haiku",  # $0.25/1M tokens - fast summaries
            "analysis": "google/gemini-pro",  # $0.50/1M tokens - deep analysis
            "comparison": "meta-llama/llama-3.1-8b-instruct",  # $0.18/1M tokens - comparisons
            "qa": "anthropic/claude-3-haiku",  # $0.25/1M tokens - Q&A
            "critique": "anthropic/claude-3.5-sonnet"  # $3/1M tokens - premium critique (limited use)
        }
        
        # Token limits for cost control
        self.token_limits = {
            "search": 1000,
            "summary": 2000,
            "analysis": 3000,
            "comparison": 2500,
            "qa": 1500,
            "critique": 1000  # Limited for cost control
        }
        
        # Track usage for budget management
        self.usage_tracker = {
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "requests": 0
        }
    
    async def analyze_paper_comprehensive(self, paper_content: str, paper_title: str = "") -> Dict[str, Any]:
        """
        Comprehensive paper analysis using multiple AI models
        """
        try:
            logger.info("Starting comprehensive paper analysis with OpenRouter")
            
            # Truncate content to manage costs
            content = self._smart_truncate(paper_content, max_tokens=8000)
            
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "paper_title": paper_title,
                "paper_length": len(paper_content),
                "analysis": {},
                "metadata": self._extract_metadata(paper_content)
            }
            
            # Parallel analysis with different models
            tasks = [
                self._generate_summary(content),
                self._extract_key_insights(content),
                self._analyze_methodology(content),
                self._generate_qa_pairs(content),
                self._assess_novelty(content)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            analysis_results["analysis"] = {
                "summary": results[0] if not isinstance(results[0], Exception) else "Summary generation failed",
                "key_insights": results[1] if not isinstance(results[1], Exception) else [],
                "methodology": results[2] if not isinstance(results[2], Exception) else "Methodology analysis failed",
                "qa_pairs": results[3] if not isinstance(results[3], Exception) else [],
                "novelty_assessment": results[4] if not isinstance(results[4], Exception) else "Novelty assessment failed"
            }
            
            logger.info(f"Analysis completed. Usage: {self.usage_tracker}")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {str(e)}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    async def _generate_summary(self, content: str) -> str:
        """Generate intelligent summary using Claude Haiku"""
        prompt = f"""Analyze this research paper and provide a concise, professional summary covering:
1. Main contribution and novelty
2. Key methodology
3. Primary results
4. Significance to the field

Paper content:
{content[:3000]}

Provide a structured summary in 150-200 words."""

        return await self._call_openrouter(
            model=self.models["summary"],
            prompt=prompt,
            max_tokens=self.token_limits["summary"]
        )
    
    async def _extract_key_insights(self, content: str) -> List[str]:
        """Extract key insights using Gemini Pro"""
        prompt = f"""Extract the 5 most important insights from this research paper. 
Focus on:
- Novel findings
- Methodological innovations
- Practical implications
- Theoretical contributions
- Future research directions

Paper content:
{content[:3000]}

Return as a numbered list of insights."""

        response = await self._call_openrouter(
            model=self.models["analysis"],
            prompt=prompt,
            max_tokens=self.token_limits["analysis"]
        )
        
        # Parse into list
        return self._parse_insights(response)
    
    async def _analyze_methodology(self, content: str) -> str:
        """Analyze methodology using Llama 3.1"""
        prompt = f"""Analyze the methodology of this research paper. Provide:
1. Research approach and design
2. Data collection methods
3. Analysis techniques
4. Strengths and potential limitations
5. Reproducibility assessment

Paper content:
{content[:3000]}

Provide a structured methodology analysis."""

        return await self._call_openrouter(
            model=self.models["comparison"],
            prompt=prompt,
            max_tokens=self.token_limits["comparison"]
        )
    
    async def _generate_qa_pairs(self, content: str) -> List[Dict[str, str]]:
        """Generate Q&A pairs using Claude Haiku"""
        prompt = f"""Generate 5 important question-answer pairs about this research paper.
Focus on questions that would help someone understand:
- The main problem being solved
- The approach used
- Key findings
- Implications
- Limitations

Paper content:
{content[:2000]}

Format as Q1: [question] A1: [answer]"""

        response = await self._call_openrouter(
            model=self.models["qa"],
            prompt=prompt,
            max_tokens=self.token_limits["qa"]
        )
        
        return self._parse_qa_pairs(response)
    
    async def _assess_novelty(self, content: str) -> str:
        """Assess novelty and significance using GPT-4o-mini"""
        prompt = f"""Assess the novelty and significance of this research paper:
1. What is novel about this work?
2. How does it advance the field?
3. What are the potential impacts?
4. Are there any overclaims or limitations?
5. Rate significance (1-5 scale) with justification

Paper content:
{content[:2000]}

Provide a balanced assessment."""

        return await self._call_openrouter(
            model=self.models["search"],
            prompt=prompt,
            max_tokens=self.token_limits["search"]
        )
    
    async def compare_papers(self, papers: List[Dict[str, str]]) -> Dict[str, Any]:
        """Compare multiple papers using Llama 3.1"""
        if len(papers) < 2:
            return {"error": "Need at least 2 papers for comparison"}
        
        comparison_prompt = f"""Compare these research papers across:
1. Problem focus and scope
2. Methodological approaches
3. Key findings and results
4. Strengths and weaknesses
5. Complementary insights

Papers:
"""
        
        for i, paper in enumerate(papers[:3]):  # Limit to 3 papers for cost
            comparison_prompt += f"\nPaper {i+1}: {paper.get('title', 'Unknown')}\n{paper.get('content', '')[:1000]}\n"
        
        comparison_prompt += "\nProvide a structured comparison highlighting similarities, differences, and complementary insights."
        
        comparison = await self._call_openrouter(
            model=self.models["comparison"],
            prompt=comparison_prompt,
            max_tokens=self.token_limits["comparison"]
        )
        
        return {
            "comparison": comparison,
            "papers_compared": len(papers),
            "timestamp": datetime.now().isoformat()
        }
    
    async def generate_critique(self, content: str, title: str = "") -> Dict[str, Any]:
        """Generate detailed critique using Claude 3.5 Sonnet (premium model - limited use)"""
        if self.usage_tracker["estimated_cost"] > 1.5:  # Budget protection
            return {"error": "Budget limit reached for premium critique"}
        
        critique_prompt = f"""As an expert peer reviewer, provide a detailed critique of this paper:

Title: {title}

Paper content:
{content[:2000]}

Provide:
1. STRENGTHS (3-4 points)
2. WEAKNESSES (3-4 points)
3. TECHNICAL ISSUES (if any)
4. CLARITY AND PRESENTATION
5. SIGNIFICANCE AND IMPACT
6. RECOMMENDATION (Accept/Minor Revision/Major Revision/Reject)

Be constructive and specific."""

        critique = await self._call_openrouter(
            model=self.models["critique"],
            prompt=critique_prompt,
            max_tokens=self.token_limits["critique"]
        )
        
        return {
            "critique": critique,
            "reviewer_mode": True,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _call_openrouter(self, model: str, prompt: str, max_tokens: int = 1000) -> str:
        """Make API call to OpenRouter"""
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Track usage
                        if "usage" in data:
                            usage = data["usage"]
                            self.usage_tracker["total_tokens"] += usage.get("total_tokens", 0)
                            self.usage_tracker["requests"] += 1
                            
                            # Rough cost estimation (varies by model)
                            estimated_cost = usage.get("total_tokens", 0) * 0.0005  # Average estimate
                            self.usage_tracker["estimated_cost"] += estimated_cost
                        
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                        return f"API Error: {response.status}"
                        
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {str(e)}")
            return f"Request failed: {str(e)}"
    
    def _smart_truncate(self, content: str, max_tokens: int = 8000) -> str:
        """Smart truncation preserving important sections"""
        # Rough token estimation (1 token ≈ 4 characters)
        max_chars = max_tokens * 4
        
        if len(content) <= max_chars:
            return content
        
        # Try to preserve abstract, introduction, and conclusion
        sections = ["abstract", "introduction", "conclusion", "results"]
        preserved_content = ""
        
        content_lower = content.lower()
        for section in sections:
            start_idx = content_lower.find(section)
            if start_idx != -1:
                # Extract section (roughly)
                end_idx = min(start_idx + 1000, len(content))
                section_content = content[start_idx:end_idx]
                if len(preserved_content + section_content) < max_chars:
                    preserved_content += section_content + "\n\n"
        
        if len(preserved_content) < max_chars // 2:
            # If sections not found, take beginning and end
            half_chars = max_chars // 2
            preserved_content = content[:half_chars] + "\n...\n" + content[-half_chars:]
        
        return preserved_content[:max_chars]
    
    def _parse_insights(self, text: str) -> List[str]:
        """Parse insights from response"""
        insights = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Clean up formatting
                clean_line = line.lstrip('0123456789.-• ').strip()
                if len(clean_line) > 10:
                    insights.append(clean_line)
        
        return insights[:5]  # Limit to 5 insights
    
    def _parse_qa_pairs(self, text: str) -> List[Dict[str, str]]:
        """Parse Q&A pairs from response"""
        qa_pairs = []
        lines = text.split('\n')
        
        current_q = ""
        current_a = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q') and ':' in line:
                if current_q and current_a:
                    qa_pairs.append({"question": current_q, "answer": current_a})
                current_q = line.split(':', 1)[1].strip()
                current_a = ""
            elif line.startswith('A') and ':' in line:
                current_a = line.split(':', 1)[1].strip()
        
        if current_q and current_a:
            qa_pairs.append({"question": current_q, "answer": current_a})
        
        return qa_pairs[:5]
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from paper"""
        return {
            "word_count": len(content.split()),
            "estimated_pages": max(1, len(content) // 3000),
            "has_abstract": "abstract" in content.lower()[:2000],
            "has_references": "references" in content.lower()[-3000:],
            "has_methodology": any(term in content.lower() for term in ["method", "approach", "experiment"]),
            "has_results": any(term in content.lower() for term in ["result", "finding", "outcome"]),
            "language": "english",
            "estimated_reading_time": len(content.split()) // 200  # words per minute
        }
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return {
            **self.usage_tracker,
            "budget_remaining": max(0, 2.0 - self.usage_tracker["estimated_cost"]),
            "models_available": list(self.models.keys())
        }
    
    async def search_arxiv_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search arXiv papers using AI-enhanced query processing"""
        # This would integrate with arXiv API
        # For now, return placeholder
        return [
            {
                "title": f"Sample Paper for: {query}",
                "authors": ["Author 1", "Author 2"],
                "abstract": "This is a sample abstract...",
                "url": "https://arxiv.org/abs/sample",
                "published": "2024-01-01"
            }
        ]



