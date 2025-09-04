#!/usr/bin/env python3
"""
Data Visualizer Service
Creates charts and visualizations from research paper analysis
"""

import plotly.graph_objects as go
import plotly.express as px
import plotly.utils
import json
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

class DataVisualizer:
    """Service for creating data visualizations from paper analysis"""
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'accent': '#2ca02c',
            'highlight': '#d62728',
            'neutral': '#7f7f7f'
        }
        
        self.chart_templates = {
            'simple': 'plotly_white',
            'dark': 'plotly_dark',
            'scientific': 'plotly_white'
        }
    
    async def create_charts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive visualizations from paper analysis data
        
        Args:
            data: Analysis data from LLM analyzer
            
        Returns:
            Dict: Chart data and configurations
        """
        try:
            logger.info("Creating visualizations from analysis data")
            
            charts = {
                "timestamp": datetime.now().isoformat(),
                "charts": {}
            }
            
            # Create different types of charts
            if "analysis" in data:
                charts["charts"]["summary_chart"] = await self._create_summary_chart(data["analysis"])
                charts["charts"]["key_points_chart"] = await self._create_key_points_chart(data["analysis"])
                charts["charts"]["methodology_chart"] = await self._create_methodology_chart(data["analysis"])
            
            if "metadata" in data:
                charts["charts"]["metadata_chart"] = await self._create_metadata_chart(data["metadata"])
            
            # Create word cloud if text content is available
            if "paper_content" in data:
                charts["charts"]["word_cloud"] = await self._create_word_cloud(data["paper_content"])
            
            logger.info("Visualizations created successfully")
            return charts
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {str(e)}")
            return {"error": f"Visualization creation failed: {str(e)}"}
    
    async def _create_summary_chart(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary visualization chart"""
        try:
            # Extract summary length and key metrics
            summary = analysis.get("summary", "")
            summary_length = len(summary)
            
            # Create a simple bar chart showing summary statistics
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Summary Length'],
                y=[summary_length],
                marker_color=self.color_scheme['primary'],
                name='Summary Length'
            ))
            
            fig.update_layout(
                title="Paper Summary Analysis",
                xaxis_title="Metric",
                yaxis_title="Value",
                template=self.chart_templates['scientific'],
                height=400
            )
            
            return {
                "type": "bar",
                "data": json.loads(fig.to_json()),
                "title": "Paper Summary Analysis"
            }
            
        except Exception as e:
            logger.warning(f"Summary chart creation failed: {str(e)}")
            return {"error": f"Summary chart error: {str(e)}"}
    
    async def _create_key_points_chart(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a chart for key points visualization"""
        try:
            key_points = analysis.get("key_points", [])
            
            if not key_points:
                return {"error": "No key points available for visualization"}
            
            # Create a horizontal bar chart for key points
            fig = go.Figure()
            
            # Count words in each key point for visualization
            point_lengths = [len(point.split()) for point in key_points]
            point_labels = [f"Point {i+1}" for i in range(len(key_points))]
            
            fig.add_trace(go.Bar(
                y=point_labels,
                x=point_lengths,
                orientation='h',
                marker_color=self.color_scheme['secondary'],
                text=point_lengths,
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Key Points Analysis",
                xaxis_title="Word Count",
                yaxis_title="Key Points",
                template=self.chart_templates['scientific'],
                height=max(400, len(key_points) * 80)
            )
            
            return {
                "type": "horizontal_bar",
                "data": json.loads(fig.to_json()),
                "title": "Key Points Analysis"
            }
            
        except Exception as e:
            logger.warning(f"Key points chart creation failed: {str(e)}")
            return {"error": f"Key points chart error: {str(e)}"}
    
    async def _create_methodology_chart(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a methodology analysis chart"""
        try:
            methodology = analysis.get("methodology", "")
            
            if not methodology:
                return {"error": "No methodology data available"}
            
            # Create a pie chart showing methodology components
            # This is a simplified analysis - in practice, you'd use NLP to categorize
            methodology_length = len(methodology)
            
            # Simple categorization based on length
            categories = {
                "Detailed": methodology_length if methodology_length > 500 else 0,
                "Moderate": methodology_length if 200 <= methodology_length <= 500 else 0,
                "Brief": methodology_length if methodology_length < 200 else 0
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(categories.keys()),
                values=list(categories.values()),
                hole=0.3,
                marker_colors=[self.color_scheme['primary'], self.color_scheme['secondary'], self.color_scheme['accent']]
            )])
            
            fig.update_layout(
                title="Methodology Analysis",
                template=self.chart_templates['scientific'],
                height=400
            )
            
            return {
                "type": "pie",
                "data": json.loads(fig.to_json()),
                "title": "Methodology Analysis"
            }
            
        except Exception as e:
            logger.warning(f"Methodology chart creation failed: {str(e)}")
            return {"error": f"Methodology chart error: {str(e)}"}
    
    async def _create_metadata_chart(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a metadata visualization chart"""
        try:
            # Create a radar chart for metadata
            categories = list(metadata.keys())
            values = []
            
            # Normalize values for radar chart
            for key in categories:
                value = metadata[key]
                if isinstance(value, bool):
                    values.append(1 if value else 0)
                elif isinstance(value, int):
                    # Normalize to 0-1 range
                    if key == "word_count":
                        values.append(min(1.0, value / 10000))  # Normalize to 10k words
                    elif key == "estimated_pages":
                        values.append(min(1.0, value / 50))  # Normalize to 50 pages
                    else:
                        values.append(min(1.0, value / 100))
                else:
                    values.append(0.5)  # Default value for strings
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Paper Metrics',
                line_color=self.color_scheme['primary']
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                title="Paper Metadata Overview",
                template=self.chart_templates['scientific'],
                height=500
            )
            
            return {
                "type": "radar",
                "data": json.loads(fig.to_json()),
                "title": "Paper Metadata Overview"
            }
            
        except Exception as e:
            logger.warning(f"Metadata chart creation failed: {str(e)}")
            return {"error": f"Metadata chart error: {str(e)}"}
    
    async def _create_word_cloud(self, text: str) -> Dict[str, Any]:
        """Create a word frequency chart (word cloud alternative)"""
        try:
            # Simple word frequency analysis
            words = text.lower().split()
            
            # Remove common stop words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
            }
            
            word_freq = {}
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top 20 words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
            
            if not top_words:
                return {"error": "No significant words found for visualization"}
            
            words_list, freq_list = zip(*top_words)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=words_list,
                y=freq_list,
                marker_color=self.color_scheme['accent'],
                text=freq_list,
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Most Frequent Words",
                xaxis_title="Words",
                yaxis_title="Frequency",
                template=self.chart_templates['scientific'],
                height=500,
                xaxis_tickangle=-45
            )
            
            return {
                "type": "bar",
                "data": json.loads(fig.to_json()),
                "title": "Most Frequent Words"
            }
            
        except Exception as e:
            logger.warning(f"Word cloud creation failed: {str(e)}")
            return {"error": f"Word cloud error: {str(e)}"}
    
    async def create_custom_chart(self, chart_type: str, data: Dict[str, Any], 
                                 custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a custom chart based on user specifications"""
        try:
            if chart_type == "line":
                return await self._create_line_chart(data, custom_config)
            elif chart_type == "scatter":
                return await self._create_scatter_chart(data, custom_config)
            elif chart_type == "heatmap":
                return await self._create_heatmap_chart(data, custom_config)
            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
                
        except Exception as e:
            logger.error(f"Custom chart creation failed: {str(e)}")
            return {"error": f"Custom chart error: {str(e)}"}
    
    async def _create_line_chart(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a line chart"""
        try:
            # Default configuration
            default_config = {
                "x_label": "X Axis",
                "y_label": "Y Axis",
                "title": "Line Chart"
            }
            
            if config:
                default_config.update(config)
            
            # This is a placeholder - you'd implement based on actual data structure
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=[1, 4, 9, 16, 25],
                mode='lines+markers',
                name='Sample Data'
            ))
            
            fig.update_layout(
                title=default_config["title"],
                xaxis_title=default_config["x_label"],
                yaxis_title=default_config["y_label"],
                template=self.chart_templates['scientific']
            )
            
            return {
                "type": "line",
                "data": json.loads(fig.to_json()),
                "title": default_config["title"]
            }
            
        except Exception as e:
            return {"error": f"Line chart error: {str(e)}"}
    
    async def _create_scatter_chart(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a scatter plot"""
        try:
            # Placeholder implementation
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=[2, 4, 1, 3, 5],
                mode='markers',
                marker=dict(size=10, color=self.color_scheme['highlight'])
            ))
            
            fig.update_layout(
                title="Scatter Plot",
                template=self.chart_templates['scientific']
            )
            
            return {
                "type": "scatter",
                "data": json.loads(fig.to_json()),
                "title": "Scatter Plot"
            }
            
        except Exception as e:
            return {"error": f"Scatter chart error: {str(e)}"}
    
    async def _create_heatmap_chart(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a heatmap chart"""
        try:
            # Placeholder implementation
            import numpy as np
            
            # Create sample data
            z_data = np.random.rand(5, 5)
            
            fig = go.Figure(data=go.Heatmap(
                z=z_data,
                colorscale='Viridis'
            ))
            
            fig.update_layout(
                title="Heatmap",
                template=self.chart_templates['scientific']
            )
            
            return {
                "type": "heatmap",
                "data": json.loads(fig.to_json()),
                "title": "Heatmap"
            }
            
        except Exception as e:
            return {"error": f"Heatmap error: {str(e)}"}
    
    def get_available_chart_types(self) -> List[str]:
        """Get list of available chart types"""
        return [
            "bar", "horizontal_bar", "line", "scatter", "pie", "radar", 
            "heatmap", "word_cloud", "summary", "key_points", "methodology", "metadata"
        ]
    
    def get_chart_templates(self) -> List[str]:
        """Get available chart templates"""
        return list(self.chart_templates.keys())
