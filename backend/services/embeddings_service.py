#!/usr/bin/env python3
"""
Embeddings Service
Handles generation of embeddings for research papers using free models
"""

import requests
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

logger = logging.getLogger(__name__)

class EmbeddingsService:
    """Service for generating paper embeddings using free models"""
    
    def __init__(self):
        """Initialize embeddings model"""
        # Use BERT-based model for embeddings (free and effective)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Check if GPU is available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        
        logger.info(f"Embeddings service initialized using device: {self.device}")
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text
        
        Args:
            text: Input text to generate embeddings for
        """
        try:
            # Generate embeddings
            embeddings = self.model.encode(
                text,
                convert_to_tensor=True,
                device=self.device
            )
            
            # Convert to list and normalize
            embeddings_list = embeddings.cpu().numpy().tolist()
            
            return embeddings_list
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return []
    
    async def generate_paper_embeddings(self, 
                                      title: str,
                                      abstract: str,
                                      full_text: Optional[str] = None) -> List[float]:
        """
        Generate embeddings for a research paper
        
        Args:
            title: Paper title
            abstract: Paper abstract
            full_text: Optional full text of paper
        """
        try:
            # Combine paper components with weights
            text_parts = [
                title * 2,  # Give more weight to title
                abstract
            ]
            
            if full_text:
                # Take first 1000 chars of full text to avoid token limits
                text_parts.append(full_text[:1000])
            
            combined_text = " ".join(text_parts)
            
            return await self.generate_embeddings(combined_text)
            
        except Exception as e:
            logger.error(f"Error generating paper embeddings: {str(e)}")
            return []
    
    async def generate_query_embeddings(self, query: str) -> List[float]:
        """
        Generate embeddings for a search query
        
        Args:
            query: Search query text
        """
        try:
            return await self.generate_embeddings(query)
        except Exception as e:
            logger.error(f"Error generating query embeddings: {str(e)}")
            return []
