#!/usr/bin/env python3
"""
RAG Service - Simplified version using only OpenRouter
"""

import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGService:
    """Service for paper analysis using OpenRouter models"""
    
    def __init__(self, openrouter_key: str):
        """Initialize with OpenRouter configuration"""
        self.openrouter_key = openrouter_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "HTTP-Referer": "https://arxivmind.com",
            "X-Title": "ArxivMind",
            "Content-Type": "application/json"
        }
        # Using free Mistral model
        self.model = "mistralai/mistral-small-3.1-24b-instruct:free"
        logger.info("RAG service initialized")

    async def analyze_paper(self, paper_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single paper"""
        try:
            analysis_type = metadata.get('analysis_type', 'comprehensive')
            
            if analysis_type == 'quick':
                prompt = f"""Analyze this research paper briefly:

Title: {metadata.get('title', 'Unknown')}
Authors: {', '.join(metadata.get('authors', []))}

Content:
{paper_content[:1500]}...

Provide a quick analysis with:
1. Summary (1-2 paragraphs)
2. Key points (2-3 bullets)
3. Main methodology
4. Main contribution

Keep the response concise and focused."""
            else:
                prompt = f"""Analyze this research paper in detail, focusing especially on the summary and novelty:

Title: {metadata.get('title', 'Unknown')}
Authors: {', '.join(metadata.get('authors', []))}

Content:
{paper_content[:2000]}...

[SUMMARY]
Provide a detailed 2-3 paragraph summary that covers:
- Main objectives and research problem
- Key methodologies and approaches used
- Significant findings and their implications
- Overall contribution to the field

[KEY CONTRIBUTIONS]
- List the main contributions and findings
- Highlight breakthrough results

[METHODOLOGY]
- Describe the technical approach
- List key techniques

[NOVELTY]
Provide a detailed analysis of the paper's novelty:
- What makes this work innovative and unique
- How it advances the state of the art
- Comparison with existing approaches
- Potential impact on the field

[Q&A]
- Key limitations
- Future directions"""

            analysis = await self._call_mistral(prompt)
            
            return {
                'paper_id': metadata.get('paper_id'),
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error analyzing paper: {str(e)}")
            raise

    async def compare_papers(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple papers"""
        try:
            # Build comparison prompt
            prompt = "Compare and analyze these research papers:\n\n"
            
            for i, paper in enumerate(papers, 1):
                prompt += f"""Paper {i}:
Title: {paper.get('title', 'Unknown')}
Authors: {', '.join(paper.get('authors', []))}
Abstract: {paper.get('abstract', '')[:500]}...\n\n"""

            prompt += """Please provide:
1. Key similarities and differences in:
   - Methodology
   - Findings
   - Applications
2. How these papers relate to each other
3. Combined insights and implications
4. Suggestions for future research

Format your response in clear sections."""

            analysis = await self._call_mistral(prompt)
            
            return {
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error comparing papers: {str(e)}")
            raise

    async def generate_insights(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights for a paper"""
        try:
            prompt = f"""Generate detailed insights for this research paper:

Title: {paper.get('title', 'Unknown')}
Authors: {', '.join(paper.get('authors', []))}
Abstract: {paper.get('abstract', '')[:500]}...

Please provide:
1. Novel contributions and key findings
2. Technical insights and methodology analysis
3. Practical applications and impact
4. Research directions and opportunities
5. Potential limitations and challenges

Format your response in clear sections with bullet points where appropriate."""

            insights = await self._call_mistral(prompt)
            
            return {
                'insights': insights,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            raise

    async def analyze(self, text: str, task: str) -> str:
        """General analysis method for any text and task"""
        try:
            prompt = f"""
Task: {task}

Text to analyze:
{text}

Please provide a comprehensive analysis based on the task requirements.
"""
            return await self._call_mistral(prompt)
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return f"Analysis failed: {str(e)}"

    async def _call_mistral(self, prompt: str) -> str:
        """Call Mistral model through OpenRouter"""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a research assistant specializing in analyzing academic papers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
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
            logger.error(f"Error calling Mistral: {str(e)}")
            raise