#!/usr/bin/env python3
"""
Paper Ingestion Service
Handles fetching and processing papers from arXiv
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import arxiv
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class PaperIngestionService:
    """Service for ingesting papers from arXiv"""
    
    def __init__(self, rag_service):
        """
        Initialize ingestion service
        
        Args:
            rag_service: RAG service instance for processing papers
        """
        self.rag_service = rag_service
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Configure arXiv client
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=3,  # Be nice to arXiv API
            num_retries=3
        )
        
        logger.info("Paper ingestion service initialized")
    
    async def ingest_papers(self, query: str, max_results: int = 10) -> List[str]:
        """
        Search and ingest papers from arXiv
        
        Args:
            query: Search query
            max_results: Maximum number of papers to ingest
        """
        try:
            # Search arXiv
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            # Fetch results
            results = await self._run_in_executor(
                lambda: list(self.client.results(search))
            )
            
            # Process papers
            paper_ids = []
            for result in results:
                try:
                    # Extract metadata
                    metadata = {
                        'paper_id': result.entry_id,
                        'title': result.title,
                        'authors': [author.name for author in result.authors],
                        'categories': result.categories,
                        'published': result.published.isoformat(),
                        'updated': result.updated.isoformat(),
                        'doi': result.doi,
                        'journal_ref': result.journal_ref,
                        'pdf_url': result.pdf_url
                    }
                    
                    # Use abstract as content (full text requires PDF processing)
                    content = result.summary
                    
                    # Process through RAG service
                    paper_id = await self.rag_service.process_paper(
                        paper_content=content,
                        metadata=metadata
                    )
                    paper_ids.append(paper_id)
                    
                except Exception as e:
                    logger.error(f"Error processing paper {result.entry_id}: {str(e)}")
                    continue
            
            return paper_ids
            
        except Exception as e:
            logger.error(f"Error ingesting papers: {str(e)}")
            raise
    
    async def ingest_recent_papers(self,
                                 categories: List[str] = None,
                                 days_back: int = 7,
                                 max_results: int = 50) -> List[str]:
        """
        Ingest recent papers from specific categories
        
        Args:
            categories: List of arXiv categories (e.g., ['cs.AI', 'cs.CL'])
            days_back: How many days back to search
            max_results: Maximum number of papers to ingest
        """
        try:
            if not categories:
                categories = ['cs.AI', 'cs.CL', 'cs.LG']  # Default to AI/ML categories
            
            # Build category filter
            category_filter = ' OR '.join(f'cat:{cat}' for cat in categories)
            
            # Calculate date range
            date_since = datetime.now() - timedelta(days=days_back)
            date_filter = f'submittedDate:[{date_since.strftime("%Y%m%d")}000000 TO *]'
            
            # Combine filters
            query = f'({category_filter}) AND {date_filter}'
            
            # Search and ingest
            return await self.ingest_papers(query, max_results)
            
        except Exception as e:
            logger.error(f"Error ingesting recent papers: {str(e)}")
            raise
    
    async def ingest_paper_by_id(self, arxiv_id: str) -> Optional[str]:
        """
        Ingest a specific paper by arXiv ID
        
        Args:
            arxiv_id: arXiv paper ID (e.g., '2101.00123')
        """
        try:
            # Search for specific paper
            search = arxiv.Search(
                id_list=[arxiv_id],
                max_results=1
            )
            
            # Fetch result
            results = await self._run_in_executor(
                lambda: list(self.client.results(search))
            )
            
            if not results:
                raise ValueError(f"Paper {arxiv_id} not found")
            
            # Process paper
            result = results[0]
            metadata = {
                'paper_id': result.entry_id,
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'categories': result.categories,
                'published': result.published.isoformat(),
                'updated': result.updated.isoformat(),
                'doi': result.doi,
                'journal_ref': result.journal_ref,
                'pdf_url': result.pdf_url
            }
            
            # Use abstract as content
            content = result.summary
            
            # Process through RAG service
            return await self.rag_service.process_paper(
                paper_content=content,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error ingesting paper {arxiv_id}: {str(e)}")
            raise
    
    async def _run_in_executor(self, func):
        """Run blocking code in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func)
