#!/usr/bin/env python3
"""
Research Insights Page for ArxivMind
"""

import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

def show_insights_page():
    st.header("💡 Research Insights")
    
    # Input methods
    input_method = st.radio(
        "Input Method",
        ["📝 Paste Text", "📁 Upload PDF", "🔗 arXiv ID"],
        horizontal=True
    )
    
    paper_content = ""
    paper_title = ""
    
    if input_method == "📝 Paste Text":
        paper_title = st.text_input("Paper Title")
        paper_content = st.text_area(
            "Paper Content",
            height=300,
            placeholder="Paste the full text of the research paper here..."
        )
        
    elif input_method == "📁 Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=['pdf'],
            help="Upload a research paper in PDF format"
        )
        
        if uploaded_file:
            with st.spinner("📄 Processing PDF..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post("http://localhost:8000/upload-paper", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        paper_content = data.get("content", "")
                        st.success("✅ PDF processed successfully")
                    else:
                        st.error(f"PDF processing failed: {response.text}")
                except Exception as e:
                    st.error(f"Upload error: {str(e)}")
                    
    elif input_method == "🔗 arXiv ID":
        arxiv_id = st.text_input(
            "arXiv ID",
            placeholder="e.g., 2301.00001"
        )
        
        if arxiv_id and st.button("📥 Fetch Paper"):
            with st.spinner("📥 Fetching from arXiv..."):
                try:
                    response = requests.get(f"http://localhost:8000/arxiv/paper/{arxiv_id}")
                    
                    if response.status_code == 200:
                        paper_data = response.json()["paper"]
                        paper_title = paper_data["title"]
                        paper_content = paper_data["content"]
                        st.success("✅ Paper fetched successfully")
                    else:
                        st.error(f"Failed to fetch paper: {response.text}")
                except Exception as e:
                    st.error(f"Fetch error: {str(e)}")
    
    # Generate insights
    if paper_content:
        if st.button("🔍 Generate Insights", type="primary"):
            with st.spinner("🤔 Analyzing paper and generating insights..."):
                try:
                    payload = {
                        "content": paper_content,
                        "title": paper_title
                    }
                    
                    response = requests.post(
                        "http://localhost:8000/research-insights",
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        insights = response.json()
                        
                        st.success("✅ Insights Generated!")
                        
                        # Display insights in sections
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🎯 Key Research Trends")
                            st.write(insights.get("trends", ""))
                            
                            st.subheader("💡 Technical Innovations")
                            st.write(insights.get("innovations", ""))
                            
                        with col2:
                            st.subheader("🔮 Future Opportunities")
                            st.write(insights.get("opportunities", ""))
                            
                            st.subheader("🏢 Industry Impact")
                            st.write(insights.get("impact", ""))
                        
                        # Visualization section
                        st.subheader("📊 Impact Analysis")
                        
                        # Example visualization using plotly
                        if "impact_scores" in insights:
                            scores = insights["impact_scores"]
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=list(scores.keys()),
                                    y=list(scores.values()),
                                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                                )
                            ])
                            fig.update_layout(
                                title="Impact Assessment",
                                xaxis_title="Categories",
                                yaxis_title="Impact Score",
                                template="plotly_dark"
                            )
                            st.plotly_chart(fig)
                        
                        # Download option
                        st.download_button(
                            "⬇️ Download Insights Report",
                            insights.get("full_report", ""),
                            file_name=f"research_insights_{paper_title or 'paper'}.txt",
                            mime="text/plain"
                        )
                        
                    else:
                        st.error(f"Insights generation failed: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
    else:
        st.info("Please provide a paper to analyze using one of the methods above.")
