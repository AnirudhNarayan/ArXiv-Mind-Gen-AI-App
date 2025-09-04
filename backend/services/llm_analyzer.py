#!/usr/bin/env python3
"""
LLM Analyzer Service
Handles AI-powered analysis of research papers using Hugging Face models
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import time
import re

logger = logging.getLogger(__name__)

class LLMAnalyzer:
    """Service for AI-powered paper analysis using Hugging Face models"""
    
    def __init__(self):
        # Load Hugging Face token from environment
        self.hf_token = os.getenv("HF_TOKEN")
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Model configurations for different tasks
        self.models = {
            "summarization": "facebook/bart-large-cnn",
            "text_generation": "facebook/bart-large-cnn",  # Using BART for text generation too
            "question_answering": "facebook/bart-large-cnn",  # Using BART for QA
            "sentiment_analysis": "facebook/bart-large-cnn",  # Using BART for analysis
            "text_classification": "facebook/bart-large-cnn"  # Using BART for classification
        }
        
        # Analysis prompts
        self.analysis_prompts = {
            "summary": "Please provide a concise summary of this research paper, highlighting the main contributions and findings.",
            "key_points": "Extract the key points and main arguments from this research paper.",
            "methodology": "Describe the methodology and approach used in this research paper.",
            "results": "What are the main results and findings presented in this research paper?",
            "implications": "What are the implications and potential impact of this research?",
            "future_work": "What future research directions are suggested by this paper?"
        }
    
    async def analyze_paper(self, paper_content: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of research paper
        
        Args:
            paper_content: Full text content of the paper
            
        Returns:
            Dict: Analysis results
        """
        try:
            logger.info("Starting comprehensive paper analysis")
            
            # Truncate content if too long (HF API has limits)
            truncated_content = self._truncate_content(paper_content, max_length=2000)
            
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "paper_length": len(paper_content),
                "analysis": {}
            }
            
            # Perform different types of analysis
            analysis_results["analysis"]["summary"] = await self._generate_summary(truncated_content)
            analysis_results["analysis"]["key_points"] = await self._extract_key_points(truncated_content)
            analysis_results["analysis"]["methodology"] = await self._analyze_methodology(truncated_content)
            analysis_results["analysis"]["results"] = await self._analyze_results(truncated_content)
            analysis_results["analysis"]["implications"] = await self._analyze_implications(truncated_content)
            
            # Extract metadata
            analysis_results["metadata"] = self._extract_metadata(paper_content)
            
            logger.info("Paper analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in paper analysis: {str(e)}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    async def _generate_summary(self, content: str) -> str:
        """Generate a concise summary of the paper"""
        try:
            if not self.hf_token:
                return "Summary generation requires Hugging Face token"
            
            # Use summarization model
            model = self.models["summarization"]
            response = await self._call_hf_model(model, content, task="summarization")
            
            if response and "summary_text" in response:
                return response["summary_text"]
            else:
                return "Unable to generate summary at this time"
                
        except Exception as e:
            logger.warning(f"Summary generation failed: {str(e)}")
            return f"Summary generation error: {str(e)}"
    
    async def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from the paper"""
        try:
            if not self.hf_token:
                return ["Key point extraction requires Hugging Face token"]
            
            # Use text generation with specific prompt
            prompt = f"{self.analysis_prompts['key_points']}\n\nPaper content: {content[:1000]}"
            
            model = self.models["text_generation"]
            response = await self._call_hf_model(model, prompt, task="text-generation")
            
            if response and "generated_text" in response:
                # Parse the generated text into key points
                text = response["generated_text"]
                return self._parse_key_points(text)
            else:
                return ["Unable to extract key points at this time"]
                
        except Exception as e:
            logger.warning(f"Key points extraction failed: {str(e)}")
            return [f"Key points extraction error: {str(e)}"]
    
    async def _analyze_methodology(self, content: str) -> str:
        """Analyze the methodology section"""
        try:
            if not self.hf_token:
                return "Methodology analysis requires Hugging Face token"
            
            prompt = f"{self.analysis_prompts['methodology']}\n\nPaper content: {content[:1000]}"
            
            model = self.models["text_generation"]
            response = await self._call_hf_model(model, prompt, task="text-generation")
            
            if response and "generated_text" in response:
                return response["generated_text"]
            else:
                return "Unable to analyze methodology at this time"
                
        except Exception as e:
            logger.warning(f"Methodology analysis failed: {str(e)}")
            return f"Methodology analysis error: {str(e)}"
    
    async def _analyze_results(self, content: str) -> str:
        """Analyze the results section"""
        try:
            if not self.hf_token:
                return "Results analysis requires Hugging Face token"
            
            prompt = f"{self.analysis_prompts['results']}\n\nPaper content: {content[:1000]}"
            
            model = self.models["text_generation"]
            response = await self._call_hf_model(model, prompt, task="text-generation")
            
            if response and "generated_text" in response:
                return response["generated_text"]
            else:
                return "Unable to analyze results at this time"
                
        except Exception as e:
            logger.warning(f"Results analysis failed: {str(e)}")
            return f"Results analysis error: {str(e)}"
    
    async def _analyze_implications(self, content: str) -> str:
        """Analyze implications and future work"""
        try:
            if not self.hf_token:
                return "Implications analysis requires Hugging Face token"
            
            prompt = f"{self.analysis_prompts['implications']}\n\nPaper content: {content[:1000]}"
            
            model = self.models["text_generation"]
            response = await self._call_hf_model(model, prompt, task="text-generation")
            
            if response and "generated_text" in response:
                return response["generated_text"]
            else:
                return "Unable to analyze implications at this time"
                
        except Exception as e:
            logger.warning(f"Implications analysis failed: {str(e)}")
            return f"Implications analysis error: {str(e)}"
    
    async def _call_hf_model(self, model: str, inputs: str, task: str = "text-generation") -> Optional[Dict]:
        """Make API call to Hugging Face model"""
        try:
            if not self.hf_token:
                logger.error("No Hugging Face token provided")
                return None
            
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            
            # Prepare payload based on task
            if task == "summarization":
                payload = {"inputs": inputs, "parameters": {"max_length": 150, "min_length": 50}}
            elif task == "text-generation":
                payload = {"inputs": inputs, "parameters": {"max_length": 200, "temperature": 0.7}}
            else:
                payload = {"inputs": inputs}
            
            url = f"{self.base_url}/{model}"
            
            logger.info(f"Calling HF model: {model} for task: {task}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                logger.warning(f"Model {model} is loading, retrying in 10 seconds...")
                time.sleep(10)
                # Retry once
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                if response.status_code == 200:
                    return response.json()
            else:
                logger.error(f"HF API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling HF model: {str(e)}")
            return None
    
    def _truncate_content(self, content: str, max_length: int = 2000) -> str:
        """Truncate content to fit API limits"""
        if len(content) <= max_length:
            return content
        
        # Try to truncate at sentence boundaries
        sentences = content.split('. ')
        truncated = ""
        
        for sentence in sentences:
            if len(truncated + sentence) < max_length:
                truncated += sentence + ". "
            else:
                break
        
        return truncated.strip()
    
    def _parse_key_points(self, text: str) -> List[str]:
        """Parse generated text into key points"""
        # Simple parsing - split by newlines or bullet points
        points = []
        
        # Split by common separators
        for line in text.split('\n'):
            line = line.strip()
            if line and len(line) > 10:  # Filter out very short lines
                # Remove common prefixes
                line = re.sub(r'^[\d\-•\*]\s*', '', line)
                if line:
                    points.append(line)
        
        # If no good splits, try splitting by periods
        if len(points) <= 1:
            sentences = text.split('. ')
            points = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return points[:5]  # Limit to 5 key points
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract basic metadata from paper content"""
        metadata = {
            "word_count": len(content.split()),
            "estimated_pages": max(1, len(content) // 3000),  # Rough estimate
            "has_abstract": "abstract" in content.lower()[:1000],
            "has_references": "references" in content.lower()[-2000:],
            "language": "english"  # Default assumption
        }
        
        return metadata
    
    async def generate_insights(self, paper_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate insights and recommendations"""
        try:
            insights = {
                "timestamp": datetime.now().isoformat(),
                "insights": [
                    "Consider the methodology's applicability to your research area",
                    "Evaluate the statistical significance of the results",
                    "Assess the limitations mentioned in the paper",
                    "Look for potential collaboration opportunities",
                    "Consider how the findings could inform future research directions"
                ],
                "recommendations": [
                    "Read related papers cited in the references",
                    "Compare findings with similar studies in the field",
                    "Consider replicating key experiments",
                    "Explore potential applications in different domains"
                ]
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return {"error": f"Failed to generate insights: {str(e)}"}
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models for different tasks"""
        return {
            "summarization": ["facebook/bart-large-cnn", "google/pegasus-xsum"],
            "text_generation": ["microsoft/DialoGPT-medium", "gpt2"],
            "question_answering": ["deepset/roberta-base-squad2"],
            "sentiment_analysis": ["cardiffnlp/twitter-roberta-base-sentiment-latest"]
        }
