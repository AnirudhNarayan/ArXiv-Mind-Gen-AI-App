#!/usr/bin/env python3
"""
ArXiv API Service
Handles fetching and processing papers from arXiv
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class ArxivService:
    """Service for interacting with arXiv API"""
    
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.max_results_per_request = 10
        
    async def search_papers(self, 
                          query: str, 
                          max_results: int = 5,
                          sort_by: str = "relevance",
                          category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search arXiv papers
        
        Args:
            query: Search query
            max_results: Maximum number of results
            sort_by: Sort criteria (relevance, lastUpdatedDate, submittedDate)
            category: arXiv category filter (e.g., 'cs.AI', 'stat.ML')
        """
        try:
            # Build search query
            search_query = self._build_search_query(query, category)
            
            params = {
                'search_query': search_query,
                'start': 0,
                'max_results': min(max_results, self.max_results_per_request),
                'sortBy': sort_by,
                'sortOrder': 'descending'
            }
            
            logger.info(f"Searching arXiv with query: {search_query}")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            papers = self._parse_arxiv_response(response.text)
            
            logger.info(f"Found {len(papers)} papers")
            return papers
            
        except Exception as e:
            logger.error(f"Error searching arXiv: {str(e)}")
            return []
    
    async def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific paper by arXiv ID
        
        Args:
            arxiv_id: arXiv paper ID (e.g., '2301.00001' or 'cs.AI/0001001')
        """
        try:
            # Clean up ID format
            clean_id = arxiv_id.replace('arxiv:', '').replace('arXiv:', '')
            
            params = {
                'id_list': clean_id,
                'max_results': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            papers = self._parse_arxiv_response(response.text)
            
            return papers[0] if papers else None
            
        except Exception as e:
            logger.error(f"Error fetching paper {arxiv_id}: {str(e)}")
            return None
    
    async def get_recent_papers(self, 
                              category: str = "cs.AI", 
                              days_back: int = 7,
                              max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent papers from specific category
        
        Args:
            category: arXiv category
            days_back: How many days back to search
            max_results: Maximum results
        """
        try:
            # Calculate date range
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for arXiv API
            date_filter = f"submittedDate:[{start_date.strftime('%Y%m%d')}* TO {end_date.strftime('%Y%m%d')}*]"
            
            search_query = f"cat:{category} AND {date_filter}"
            
            params = {
                'search_query': search_query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            return self._parse_arxiv_response(response.text)
            
        except Exception as e:
            logger.error(f"Error fetching recent papers: {str(e)}")
            return []
    
    async def get_paper_full_text(self, paper_url: str) -> Optional[str]:
        """
        Attempt to get full text of paper
        Note: This is a simplified implementation
        """
        try:
            # Try to get PDF URL
            if 'abs/' in paper_url:
                pdf_url = paper_url.replace('/abs/', '/pdf/') + '.pdf'
            else:
                pdf_url = paper_url
            
            # For now, return placeholder - would need PDF parsing
            return f"Full text extraction from {pdf_url} would be implemented here"
            
        except Exception as e:
            logger.error(f"Error getting full text: {str(e)}")
            return None
    
    def _build_search_query(self, query: str, category: Optional[str] = None) -> str:
        """Build arXiv search query"""
        # Clean and prepare query
        clean_query = re.sub(r'[^\w\s\-\+\(\)]', '', query)
        
        # Add category filter if specified
        if category:
            search_query = f"cat:{category} AND ({clean_query})"
        else:
            search_query = clean_query
        
        return search_query
    
    def _parse_arxiv_response(self, xml_response: str) -> List[Dict[str, Any]]:
        """Parse XML response from arXiv API"""
        try:
            root = ET.fromstring(xml_response)
            
            # Define namespaces
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            papers = []
            
            for entry in root.findall('atom:entry', namespaces):
                paper = self._parse_paper_entry(entry, namespaces)
                if paper:
                    papers.append(paper)
            
            return papers
            
        except Exception as e:
            logger.error(f"Error parsing arXiv response: {str(e)}")
            return []
    
    def _parse_paper_entry(self, entry, namespaces: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Parse individual paper entry"""
        try:
            # Extract basic information
            title_elem = entry.find('atom:title', namespaces)
            title = title_elem.text.strip() if title_elem is not None else "Unknown Title"
            
            summary_elem = entry.find('atom:summary', namespaces)
            abstract = summary_elem.text.strip() if summary_elem is not None else ""
            
            # Extract authors
            authors = []
            for author in entry.findall('atom:author', namespaces):
                name_elem = author.find('atom:name', namespaces)
                if name_elem is not None:
                    authors.append(name_elem.text.strip())
            
            # Extract dates
            published_elem = entry.find('atom:published', namespaces)
            published = published_elem.text if published_elem is not None else ""
            
            updated_elem = entry.find('atom:updated', namespaces)
            updated = updated_elem.text if updated_elem is not None else ""
            
            # Extract arXiv ID and URLs
            id_elem = entry.find('atom:id', namespaces)
            arxiv_url = id_elem.text if id_elem is not None else ""
            arxiv_id = self._extract_arxiv_id(arxiv_url)
            
            # Extract categories
            categories = []
            for category in entry.findall('atom:category', namespaces):
                term = category.get('term')
                if term:
                    categories.append(term)
            
            # Extract primary category
            primary_category_elem = entry.find('arxiv:primary_category', namespaces)
            primary_category = primary_category_elem.get('term') if primary_category_elem is not None else ""
            
            # Extract DOI if available
            doi_elem = entry.find('arxiv:doi', namespaces)
            doi = doi_elem.text if doi_elem is not None else ""
            
            # Extract comment
            comment_elem = entry.find('arxiv:comment', namespaces)
            comment = comment_elem.text if comment_elem is not None else ""
            
            # Build paper dictionary
            paper = {
                'id': arxiv_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'published': published,
                'updated': updated,
                'url': arxiv_url,
                'pdf_url': arxiv_url.replace('/abs/', '/pdf/') + '.pdf' if '/abs/' in arxiv_url else '',
                'categories': categories,
                'primary_category': primary_category,
                'doi': doi,
                'comment': comment,
                'summary_stats': {
                    'abstract_length': len(abstract.split()),
                    'author_count': len(authors),
                    'category_count': len(categories)
                }
            }
            
            return paper
            
        except Exception as e:
            logger.error(f"Error parsing paper entry: {str(e)}")
            return None
    
    def _extract_arxiv_id(self, url: str) -> str:
        """Extract arXiv ID from URL"""
        try:
            # Handle different URL formats
            if '/abs/' in url:
                return url.split('/abs/')[-1]
            elif '/pdf/' in url:
                return url.split('/pdf/')[-1].replace('.pdf', '')
            else:
                # Try to extract ID pattern
                import re
                match = re.search(r'(\d{4}\.\d{4,5})', url)
                return match.group(1) if match else url
        except:
            return url
    
    def get_category_info(self) -> Dict[str, Dict[str, str]]:
        """Get information about arXiv categories"""
        return {
            'cs': {
                'name': 'Computer Science',
                'subcategories': {
                    'cs.AI': 'Artificial Intelligence',
                    'cs.CL': 'Computation and Language',
                    'cs.CV': 'Computer Vision and Pattern Recognition',
                    'cs.LG': 'Machine Learning',
                    'cs.NE': 'Neural and Evolutionary Computing',
                    'cs.RO': 'Robotics',
                    'cs.DS': 'Data Structures and Algorithms'
                }
            },
            'stat': {
                'name': 'Statistics',
                'subcategories': {
                    'stat.ML': 'Machine Learning',
                    'stat.AP': 'Applications',
                    'stat.CO': 'Computation',
                    'stat.ME': 'Methodology'
                }
            },
            'math': {
                'name': 'Mathematics',
                'subcategories': {
                    'math.ST': 'Statistics Theory',
                    'math.OC': 'Optimization and Control',
                    'math.PR': 'Probability'
                }
            },
            'physics': {
                'name': 'Physics',
                'subcategories': {
                    'physics.data-an': 'Data Analysis, Statistics and Probability'
                }
            }
        }
    
    def suggest_categories(self, query: str) -> List[str]:
        """Suggest relevant categories based on query"""
        query_lower = query.lower()
        suggestions = []
        
        # AI/ML related
        if any(term in query_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural']):
            suggestions.extend(['cs.AI', 'cs.LG', 'stat.ML'])
        
        # Computer Vision
        if any(term in query_lower for term in ['computer vision', 'image', 'visual', 'cv']):
            suggestions.append('cs.CV')
        
        # NLP
        if any(term in query_lower for term in ['nlp', 'language', 'text', 'linguistic']):
            suggestions.append('cs.CL')
        
        # Robotics
        if any(term in query_lower for term in ['robot', 'robotics', 'autonomous']):
            suggestions.append('cs.RO')
        
        # Default to AI if nothing specific
        if not suggestions:
            suggestions.append('cs.AI')
        
        return suggestions[:3]  # Limit to top 3 suggestions



