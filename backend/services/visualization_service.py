"""
Visualization service for ArxivMind
Handles data processing and analytics for various visualizations
"""

from typing import Dict, List, Any
import pandas as pd
from collections import Counter
import networkx as nx
from datetime import datetime, timedelta

class VisualizationService:
    def __init__(self):
        self.cache = {}  # Simple cache for results
        
    def get_topic_distribution(self, papers: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Analyze papers and return topic distribution
        """
        topics = []
        for paper in papers:
            # Extract topics from paper keywords and categories
            paper_topics = paper.get('categories', []) + paper.get('keywords', [])
            topics.extend(paper_topics)
            
        # Count topic frequencies
        topic_counts = Counter(topics)
        return dict(topic_counts.most_common(10))
    
    def build_citation_network(self, papers: List[Dict[str, Any]]) -> Dict[str, List]:
        """
        Build citation network from papers
        """
        G = nx.DiGraph()
        
        # Add nodes and edges
        for paper in papers:
            paper_id = paper.get('id')
            G.add_node(paper_id)
            
            # Add citation edges
            for cited_paper in paper.get('references', []):
                G.add_edge(paper_id, cited_paper)
        
        # Convert to format suitable for visualization
        nodes = list(G.nodes())
        edges = list(G.edges())
        weights = [G.degree(node) for node in nodes]
        
        return {
            'nodes': nodes,
            'edges': edges,
            'weights': weights
        }
    
    def compare_methodologies(self, papers: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """
        Compare different methodologies used in papers
        """
        methods = {}
        
        for paper in papers:
            method = paper.get('methodology', '')
            if method:
                if method not in methods:
                    methods[method] = {
                        'accuracy': [],
                        'speed': [],
                        'resource_usage': []
                    }
                
                # Extract or estimate metrics
                metrics = paper.get('metrics', {})
                methods[method]['accuracy'].append(metrics.get('accuracy', 0))
                methods[method]['speed'].append(metrics.get('speed', 0))
                methods[method]['resource_usage'].append(metrics.get('resource_usage', 0))
        
        # Calculate averages
        result = {
            'Method': [],
            'Accuracy': [],
            'Speed': [],
            'Resource Usage': []
        }
        
        for method, metrics in methods.items():
            result['Method'].append(method)
            result['Accuracy'].append(sum(metrics['accuracy']) / len(metrics['accuracy']) if metrics['accuracy'] else 0)
            result['Speed'].append(sum(metrics['speed']) / len(metrics['speed']) if metrics['speed'] else 0)
            result['Resource Usage'].append(sum(metrics['resource_usage']) / len(metrics['resource_usage']) if metrics['resource_usage'] else 0)
        
        return result
    
    def calculate_research_impact(self, papers: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate various research impact metrics
        """
        total_citations = sum(paper.get('citations', 0) for paper in papers)
        total_downloads = sum(paper.get('downloads', 0) for paper in papers)
        social_media_mentions = sum(paper.get('social_media_mentions', 0) for paper in papers)
        industry_uses = sum(paper.get('industry_uses', 0) for paper in papers)
        academic_uses = sum(paper.get('academic_uses', 0) for paper in papers)
        
        # Normalize scores to 0-100 scale
        max_value = max(total_citations, total_downloads, social_media_mentions, 
                       industry_uses, academic_uses)
        
        return {
            'Citations': (total_citations / max_value) * 100 if max_value > 0 else 0,
            'Downloads': (total_downloads / max_value) * 100 if max_value > 0 else 0,
            'Social Media': (social_media_mentions / max_value) * 100 if max_value > 0 else 0,
            'Industry Use': (industry_uses / max_value) * 100 if max_value > 0 else 0,
            'Academic Use': (academic_uses / max_value) * 100 if max_value > 0 else 0
        }
    
    def analyze_temporal_trends(self, papers: List[Dict[str, Any]]) -> Dict[str, List]:
        """
        Analyze research trends over time
        """
        # Create timeline
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*3)  # Last 3 years
        timeline = pd.date_range(start=start_date, end=end_date, freq='Q')
        
        # Initialize trend data
        trends = {
            'Date': timeline,
            'ML': [0] * len(timeline),
            'CV': [0] * len(timeline),
            'NLP': [0] * len(timeline)
        }
        
        # Count papers by category and date
        for paper in papers:
            pub_date = paper.get('publication_date')
            if not pub_date:
                continue
                
            pub_date = pd.to_datetime(pub_date)
            if pub_date < start_date or pub_date > end_date:
                continue
            
            # Find the quarter index
            quarter_index = 0
            for i, date in enumerate(timeline):
                if pub_date <= date:
                    quarter_index = i
                    break
            
            # Update counts based on paper categories
            categories = paper.get('categories', [])
            if 'Machine Learning' in categories or 'AI' in categories:
                trends['ML'][quarter_index] += 1
            if 'Computer Vision' in categories:
                trends['CV'][quarter_index] += 1
            if 'Natural Language Processing' in categories:
                trends['NLP'][quarter_index] += 1
        
        return trends
