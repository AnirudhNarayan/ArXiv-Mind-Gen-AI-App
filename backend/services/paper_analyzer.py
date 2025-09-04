#!/usr/bin/env python3
"""
Paper Analyzer Service
Handles paper analysis using free Mistral model
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PaperAnalyzer:
    """Service for analyzing research papers using Mistral"""
    
    def __init__(self):
        """Initialize with OpenRouter configuration"""
        self.openrouter_key = "OPENROUTER_KEY"  # Replace with your key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://arxivmind.com",
            "X-Title": "ArxivMind",
            "Content-Type": "application/json"
        }
        
        # Use Mistral Small 3.1 (free model)
        self.model = "mistralai/mistral-small-3.1-24b-instruct:free"
    
    async def generate_summary(self, paper_content: str, paper_title: str = "") -> str:
        """
        Generate a concise summary of the paper using Mistral
        
        Args:
            paper_content: Paper content or abstract
            paper_title: Optional paper title
        """
        try:
            # Craft prompt for summary
            prompt = f"""Please provide a concise, clear summary of this research paper.
            Focus on the main contributions, methodology, and key findings.
            
            Title: {paper_title}
            
            Content:
            {paper_content}
            
            Generate a summary that is:
            1. Clear and accessible
            2. Highlights key contributions
            3. Mentions main methodology
            4. States important findings
            """
            
            response = await self._call_mistral(prompt)
            return response if response else "Summary generation failed"
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Error generating summary"
    
    async def generate_qa(self, paper_content: str) -> List[Dict[str, str]]:
        """Generate Q&A pairs based on paper content"""
        try:
            prompt = f"""Based on this research paper, generate 3 important question-answer pairs
            that would help someone understand the key aspects of the work.
            
            Paper content:
            {paper_content}
            
            Format each pair as:
            Q: [Question]
            A: [Clear, concise answer]
            """
            
            response = await self._call_mistral(prompt)
            
            # Parse Q&A pairs
            qa_pairs = []
            if response:
                pairs = response.split("Q: ")
                for pair in pairs[1:]:  # Skip first empty split
                    try:
                        q, a = pair.split("A: ")
                        qa_pairs.append({
                            "question": q.strip(),
                            "answer": a.strip()
                        })
                    except:
                        continue
            
            return qa_pairs
            
        except Exception as e:
            logger.error(f"Error generating Q&A: {str(e)}")
            return []
    
    async def _call_mistral(self, prompt: str) -> Optional[str]:
        """Make API call to Mistral model"""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error calling Mistral API: {str(e)}")
            return None
