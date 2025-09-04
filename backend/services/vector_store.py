#!/usr/bin/env python3
"""
Vector Store Service
Handles storage and retrieval of research paper embeddings using ChromaDB
"""

import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Any, Optional
import os
import json

logger = logging.getLogger(__name__)

class VectorStore:
    """Service for managing research paper embeddings"""
    
    def __init__(self):
        """Initialize ChromaDB client"""
        # Initialize with persistent storage
        self.client = chromadb.PersistentClient(path="./data/vectordb")
        
        # Create collection for research papers if it doesn't exist
        self.papers_collection = self.client.get_or_create_collection(
            name="research_papers",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        logger.info("Vector store initialized successfully")
    
    async def add_paper(self, 
                       paper_id: str,
                       embeddings: List[float],
                       metadata: Dict[str, Any],
                       content: str) -> bool:
        """
        Add a paper to the vector store
        
        Args:
            paper_id: Unique identifier (e.g., arXiv ID)
            embeddings: Vector embeddings of the paper
            metadata: Paper metadata (title, authors, etc.)
            content: Paper content or abstract
        """
        try:
            self.papers_collection.add(
                ids=[paper_id],
                embeddings=[embeddings],
                metadatas=[metadata],
                documents=[content]
            )
            logger.info(f"Added paper {paper_id} to vector store")
            return True
        except Exception as e:
            logger.error(f"Error adding paper to vector store: {str(e)}")
            return False
    
    async def find_similar_papers(self,
                                embeddings: List[float],
                                n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Find similar papers using vector similarity
        
        Args:
            embeddings: Query vector embeddings
            n_results: Number of similar papers to return
        """
        try:
            results = self.papers_collection.query(
                query_embeddings=[embeddings],
                n_results=n_results,
                include=["metadatas", "documents", "distances"]
            )
            
            # Format results
            similar_papers = []
            for i in range(len(results['ids'][0])):
                paper = {
                    'id': results['ids'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'content': results['documents'][0][i],
                    'similarity': 1 - results['distances'][0][i]  # Convert distance to similarity
                }
                similar_papers.append(paper)
            
            return similar_papers
            
        except Exception as e:
            logger.error(f"Error finding similar papers: {str(e)}")
            return []
    
    async def get_paper(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific paper from the vector store"""
        try:
            result = self.papers_collection.get(
                ids=[paper_id],
                include=["metadatas", "documents"]
            )
            
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'metadata': result['metadatas'][0],
                    'content': result['documents'][0]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting paper {paper_id}: {str(e)}")
            return None
    
    async def delete_paper(self, paper_id: str) -> bool:
        """Delete a paper from the vector store"""
        try:
            self.papers_collection.delete(ids=[paper_id])
            logger.info(f"Deleted paper {paper_id} from vector store")
            return True
        except Exception as e:
            logger.error(f"Error deleting paper {paper_id}: {str(e)}")
            return False
