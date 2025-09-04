#!/usr/bin/env python3
"""
Comparative Analysis Service
Handles comparison of research papers using RAG and vector similarity
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ComparativeAnalyzer:
    """Service for comparing research papers using RAG"""
    
    def __init__(self, vector_store, embeddings_service, paper_analyzer):
        """
        Initialize with required services
        
        Args:
            vector_store: VectorStore instance
            embeddings_service: EmbeddingsService instance
            paper_analyzer: PaperAnalyzer instance
        """
        self.vector_store = vector_store
        self.embeddings_service = embeddings_service
        self.paper_analyzer = paper_analyzer
        logger.info("Comparative analyzer initialized")
    
    async def compare_papers(self,
                           paper_ids: List[str],
                           aspects: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Compare multiple papers across different aspects
        
        Args:
            paper_ids: List of paper IDs to compare
            aspects: Optional list of aspects to compare (e.g., ['methodology', 'results'])
        """
        try:
            if not aspects:
                aspects = ['methodology', 'results', 'contributions']
            
            comparison_results = {
                'timestamp': datetime.now().isoformat(),
                'papers': [],
                'comparisons': {}
            }
            
            # Fetch papers
            papers = []
            for paper_id in paper_ids:
                paper = await self.vector_store.get_paper(paper_id)
                if paper:
                    papers.append(paper)
                    comparison_results['papers'].append({
                        'id': paper['id'],
                        'title': paper['metadata'].get('title', 'Unknown'),
                        'authors': paper['metadata'].get('authors', [])
                    })
            
            # Compare each aspect
            for aspect in aspects:
                comparison_results['comparisons'][aspect] = await self._compare_aspect(
                    papers, aspect
                )
            
            # Find related papers
            related_papers = await self._find_related_papers(papers)
            comparison_results['related_papers'] = related_papers
            
            return comparison_results
            
        except Exception as e:
            logger.error(f"Error in comparative analysis: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _compare_aspect(self,
                            papers: List[Dict[str, Any]],
                            aspect: str) -> Dict[str, Any]:
        """Compare papers on a specific aspect"""
        try:
            # Generate comparison prompt
            papers_info = []
            for paper in papers:
                papers_info.append(f"""
                Title: {paper['metadata'].get('title', 'Unknown')}
                Content: {paper['content'][:1000]}  # Limit content length
                """)
            
            prompt = f"""Compare the following papers specifically focusing on their {aspect}.
            Highlight key similarities and differences.
            
            Papers:
            {"".join(papers_info)}
            
            Please provide:
            1. Key similarities in {aspect}
            2. Notable differences in {aspect}
            3. A brief comparative analysis
            """
            
            # Get comparison from Mistral
            analysis = await self.paper_analyzer._call_mistral(prompt)
            
            return {
                'analysis': analysis,
                'aspect': aspect
            }
            
        except Exception as e:
            logger.error(f"Error comparing aspect {aspect}: {str(e)}")
            return {
                'error': str(e),
                'aspect': aspect
            }
    
    async def _find_related_papers(self,
                                 papers: List[Dict[str, Any]],
                                 max_related: int = 5) -> List[Dict[str, Any]]:
        """Find papers related to the comparison set"""
        try:
            # Combine embeddings of all papers
            all_embeddings = []
            for paper in papers:
                paper_embedding = await self.embeddings_service.generate_paper_embeddings(
                    title=paper['metadata'].get('title', ''),
                    abstract=paper['content']
                )
                if paper_embedding:
                    all_embeddings.append(paper_embedding)
            
            if not all_embeddings:
                return []
            
            # Average the embeddings for similarity search
            import numpy as np
            avg_embedding = np.mean(all_embeddings, axis=0).tolist()
            
            # Find similar papers
            similar_papers = await self.vector_store.find_similar_papers(
                embeddings=avg_embedding,
                n_results=max_related
            )
            
            # Filter out papers that were in the comparison set
            paper_ids = set(p['id'] for p in papers)
            related = [
                paper for paper in similar_papers
                if paper['id'] not in paper_ids
            ]
            
            return related[:max_related]
            
        except Exception as e:
            logger.error(f"Error finding related papers: {str(e)}")
            return []
    
    async def generate_comparison_summary(self,
                                       comparison_results: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the comparison"""
        try:
            papers = comparison_results.get('papers', [])
            if not papers:
                return "No papers to compare"
            
            # Create summary prompt
            paper_titles = [f"- {p.get('title', 'Unknown')}" for p in papers]
            aspects = comparison_results.get('comparisons', {}).keys()
            
            prompt = f"""Create a clear, concise summary of the comparison between these papers:
            
            Papers compared:
            {"".join(paper_titles)}
            
            Aspects compared:
            {", ".join(aspects)}
            
            Key findings from each aspect:
            """
            
            for aspect, details in comparison_results.get('comparisons', {}).items():
                prompt += f"\n{aspect}:\n{details.get('analysis', 'No analysis available')}\n"
            
            prompt += "\nPlease provide a clear, structured summary that highlights:"
            prompt += "\n1. The most significant similarities"
            prompt += "\n2. The key differences"
            prompt += "\n3. Overall insights from the comparison"
            
            summary = await self.paper_analyzer._call_mistral(prompt)
            return summary if summary else "Failed to generate summary"
            
        except Exception as e:
            logger.error(f"Error generating comparison summary: {str(e)}")
            return f"Error generating summary: {str(e)}"
