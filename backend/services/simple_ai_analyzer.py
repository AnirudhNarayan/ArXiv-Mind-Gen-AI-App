#!/usr/bin/env python3
"""
Simple OpenAI Analyzer Service
Basic AI-powered analysis using OpenAI API with minimal credit usage
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SimpleAIAnalyzer:
    """Simple service for AI-powered paper analysis using OpenAI API"""
    
    def __init__(self):
        """Initialize with OpenAI configuration"""
        # Using OpenRouter for OpenAI access
        self.openrouter_key = "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"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://arxivmind.com",
            "X-Title": "ArxivMind",
            "Content-Type": "application/json"
        }
        
        # Use only GPT-4o-mini for cost efficiency
        self.model = "openai/gpt-4o-mini"  # Very cost-effective
        
        # Track usage for budget management
        self.usage_tracker = {
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "requests": 0
        }
    
    def analyze_paper_simple(self, paper_content: str, paper_title: str = "") -> Dict[str, Any]:
        """
        Simple paper analysis with minimal API usage
        """
        try:
            logger.info("Starting simple paper analysis")
            
            # Truncate content to save costs
            content = self._truncate_content(paper_content, max_words=1000)
            
            # Single API call for basic analysis
            prompt = f"""Analyze this research paper and provide:
1. A brief summary (2-3 sentences)
2. Key findings (3 bullet points)
3. Main contribution (1 sentence)

Paper title: {paper_title}
Paper content: {content}

Keep the response concise and focused."""

            response = self._call_openai(prompt, max_tokens=300)
            
            # Parse response
            analysis = self._parse_simple_response(response)
            
            return {
                "summary": analysis.get("summary", "Analysis completed"),
                "key_findings": analysis.get("key_findings", []),
                "main_contribution": analysis.get("main_contribution", ""),
                "paper_title": paper_title,
                "word_count": len(paper_content.split()),
                "usage_stats": self.get_usage_stats()
            }
            
        except Exception as e:
            logger.error(f"Simple analysis failed: {str(e)}")
            return {
                "summary": "Analysis failed due to an error",
                "key_findings": ["Error occurred during analysis"],
                "main_contribution": "Unable to determine",
                "error": str(e)
            }
    
    def generate_insights(self, paper_content: str) -> List[str]:
        """Generate simple insights from paper"""
        try:
            content = self._truncate_content(paper_content, max_words=800)
            
            prompt = f"""Based on this research paper, provide 3 key insights:

{content}

Format as numbered list:
1. [insight]
2. [insight] 
3. [insight]"""

            response = self._call_openai(prompt, max_tokens=200)
            
            # Extract insights from response
            insights = []
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    clean_line = line.lstrip('0123456789.-• ').strip()
                    if len(clean_line) > 10:
                        insights.append(clean_line)
            
            return insights[:3] if insights else ["Analysis completed successfully"]
            
        except Exception as e:
            logger.error(f"Insights generation failed: {str(e)}")
            return ["Unable to generate insights due to an error"]
    
    def _call_openai(self, prompt: str, max_tokens: int = 300) -> str:
        """Make API call to OpenAI via OpenRouter"""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3  # Lower temperature for consistent results
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Track usage
                if "usage" in data:
                    usage = data["usage"]
                    self.usage_tracker["total_tokens"] += usage.get("total_tokens", 0)
                    self.usage_tracker["requests"] += 1
                    
                    # Cost estimation for GPT-4o-mini ($0.15 per 1M tokens)
                    estimated_cost = usage.get("total_tokens", 0) * 0.00015 / 1000
                    self.usage_tracker["estimated_cost"] += estimated_cost
                
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}")
            return f"Request failed: {str(e)}"
    
    def _truncate_content(self, content: str, max_words: int = 1000) -> str:
        """Truncate content to save on API costs"""
        words = content.split()
        if len(words) <= max_words:
            return content
        
        # Try to keep abstract and introduction if possible
        content_lower = content.lower()
        if "abstract" in content_lower:
            abstract_start = content_lower.find("abstract")
            if abstract_start != -1:
                # Take from abstract onwards
                truncated = content[abstract_start:abstract_start + max_words * 6]  # Rough word to char conversion
                return truncated
        
        # Otherwise take first portion
        return ' '.join(words[:max_words])
    
    def _parse_simple_response(self, response: str) -> Dict[str, Any]:
        """Parse the simple analysis response"""
        result = {
            "summary": "",
            "key_findings": [],
            "main_contribution": ""
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if "summary" in line.lower() or line.startswith("1."):
                current_section = "summary"
                if ":" in line:
                    result["summary"] = line.split(":", 1)[1].strip()
                continue
            elif "key findings" in line.lower() or "findings" in line.lower() or line.startswith("2."):
                current_section = "key_findings"
                continue
            elif "contribution" in line.lower() or line.startswith("3."):
                current_section = "main_contribution"
                if ":" in line:
                    result["main_contribution"] = line.split(":", 1)[1].strip()
                continue
            
            # Add content to current section
            if current_section == "summary" and not result["summary"]:
                result["summary"] = line
            elif current_section == "key_findings" and (line.startswith("-") or line.startswith("•") or line[0].isdigit()):
                clean_line = line.lstrip('0123456789.-• ').strip()
                if clean_line:
                    result["key_findings"].append(clean_line)
            elif current_section == "main_contribution" and not result["main_contribution"]:
                result["main_contribution"] = line
        
        # Fallback if parsing fails
        if not result["summary"]:
            result["summary"] = response[:200] + "..." if len(response) > 200 else response
        
        return result
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return {
            **self.usage_tracker,
            "budget_remaining": max(0, 2.0 - self.usage_tracker["estimated_cost"]),
            "model_used": self.model,
            "cost_per_request": self.usage_tracker["estimated_cost"] / max(1, self.usage_tracker["requests"])
        }


