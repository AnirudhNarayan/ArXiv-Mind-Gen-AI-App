#!/usr/bin/env python3
"""
Compare Papers Page for ArxivMind
"""

import streamlit as st
import requests
from typing import Dict, List, Any
import json

def show_comparison_page():
    st.header("⚖️ Compare Research Papers")
    
    # Papers to compare
    papers = []
    
    # Add paper method selection
    add_method = st.radio(
        "Add Paper",
        ["📝 Paste Text", "📁 Upload PDF", "🔗 arXiv ID"],
        horizontal=True
    )
    
    if add_method == "📝 Paste Text":
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Paper Title")
        with col2:
            authors = st.text_input("Authors (comma-separated)")
        content = st.text_area("Paper Content", height=200)
        
        if st.button("➕ Add Paper"):
            if content:
                papers.append({
                    "title": title,
                    "authors": [a.strip() for a in authors.split(",")],
                    "content": content
                })
                st.success("Paper added for comparison")
            else:
                st.warning("Please provide paper content")
                
    elif add_method == "📁 Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=['pdf'],
            help="Upload a research paper in PDF format"
        )
        
        if uploaded_file:
            files = {"file": uploaded_file}
            response = requests.post("http://localhost:8000/upload-paper", files=files)
            
            if response.status_code == 200:
                data = response.json()
                papers.append({
                    "title": uploaded_file.name,
                    "content": data["content"],
                    "authors": []
                })
                st.success("PDF processed and added for comparison")
            else:
                st.error(f"PDF processing failed: {response.text}")
                
    elif add_method == "🔗 arXiv ID":
        arxiv_id = st.text_input(
            "arXiv ID",
            placeholder="e.g., 2301.00001"
        )
        
        if st.button("📥 Fetch Paper"):
            response = requests.get(f"http://localhost:8000/arxiv/paper/{arxiv_id}")
            
            if response.status_code == 200:
                paper_data = response.json()["paper"]
                papers.append({
                    "title": paper_data["title"],
                    "authors": paper_data["authors"],
                    "content": paper_data["abstract"]
                })
                st.success("Paper fetched and added for comparison")
            else:
                st.error(f"Failed to fetch paper: {response.text}")
    
    # Show added papers
    if papers:
        st.subheader("Papers to Compare")
        for i, paper in enumerate(papers, 1):
            with st.expander(f"📄 Paper {i}: {paper['title']}"):
                st.write(f"**Authors:** {', '.join(paper['authors'])}")
                st.write("**Preview:**")
                st.write(paper['content'][:500] + "...")
    
    # Compare button
    if len(papers) >= 2:
        if st.button("🔄 Compare Papers", type="primary"):
            try:
                response = requests.post(
                    "http://localhost:8000/compare-papers",
                    json=papers
                )
                
                if response.status_code == 200:
                    comparisons = response.json()["comparisons"]
                    
                    for comp in comparisons:
                        st.subheader(f"Comparison: {comp['paper1_title']} vs {comp['paper2_title']}")
                        st.write(comp["comparison"])
                else:
                    st.error(f"Comparison failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Error during comparison: {str(e)}")
    elif papers:
        st.info("Add at least one more paper to compare")
