#!/usr/bin/env python3
"""
Peer Review Page for ArxivMind
"""

import streamlit as st
import requests
from typing import Dict, Any

def show_peer_review_page():
    st.header("👩‍⚖️ Expert Peer Review")
    
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
    
        # Review options
    if paper_content:
        col1, col2 = st.columns([2, 2])
        with col1:
            review_type = st.selectbox(
                "Review Type",
                options=["Standard Review", "Detailed Analysis", "Conference Review", "Journal Review", "Technical Review"],
                index=0,
                key="review_type",
                help="Choose the depth and style of peer review"
            )        if st.button("📝 Generate Review", type="primary"):
            with st.spinner("🤔 Analyzing paper and generating review..."):
                try:
                    payload = {
                        "content": paper_content,
                        "title": paper_title,
                        "review_type": review_type
                    }
                    
                    response = requests.post(
                        "http://localhost:8000/peer-review",
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        review = response.json()
                        
                        st.success("✅ Review Generated!")
                        
                        # Display review in sections
                        st.subheader("Peer Review Results")
                        
                        with st.expander("📊 Overall Assessment", expanded=True):
                            st.write(review.get("overall_assessment", ""))
                            
                        with st.expander("🔬 Technical Evaluation"):
                            st.write(review.get("technical_evaluation", ""))
                            
                        with st.expander("📈 Results & Methodology"):
                            st.write(review.get("results_evaluation", ""))
                            
                        with st.expander("✍️ Writing & Organization"):
                            st.write(review.get("writing_evaluation", ""))
                            
                        with st.expander("💡 Recommendations"):
                            st.write(review.get("recommendations", ""))
                            
                        # Download options
                        st.download_button(
                            "⬇️ Download Review",
                            review.get("review", ""),
                            file_name=f"peer_review_{paper_title or 'paper'}.txt",
                            mime="text/plain"
                        )
                        
                    else:
                        st.error(f"Review generation failed: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error during review: {str(e)}")
    else:
        st.info("Please provide a paper to review using one of the methods above.")
