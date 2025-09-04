#!/usr/bin/env python3
"""
ArxivMind Frontend - Premium AI Research Assistant
Streamlit frontend with multi-page structure and advanced features
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="ArxivMind - AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend configuration
BACKEND_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        background-color: #1a1a1a !important;
    }
    
    /* Main app background */
    .stApp {
        background-color: #1a1a1a !important;
    }
    
    /* Main content area */
    .main {
        background-color: #1a1a1a !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%) !important;
        padding-top: 2rem !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%) !important;
        border-right: 3px solid #ffffff20 !important;
    }
    
    /* Sidebar Content */
    .css-17eq0hr {
        background: transparent !important;
    }
    
    /* Custom Navigation Buttons */
    .nav-button {
        display: block;
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
        text-decoration: none;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: left;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .nav-button.active {
        background: rgba(255, 255, 255, 0.25);
        border-color: #4CAF50;
        box-shadow: 0 0 20px rgba(76, 175, 80, 0.3);
    }
    
    /* Main Content Styling */
    .main-content {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        font-family: 'Inter', sans-serif;
    }
    
    .feature-box h2 {
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .feature-box p {
        margin: 0;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Status Cards - Dark Theme */
    .status-card {
        background: #2d2d2d;
        color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
        font-family: 'Inter', sans-serif;
    }
    
    .status-card h3 {
        color: #ffffff !important;
    }
    
    .status-card ul li {
        color: #ffffff !important;
    }
    
    /* Metric Styling - Dark Theme */
    div[data-testid="metric-container"] {
        background: #2d2d2d;
        color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #2196F3;
    }
    
    /* Comprehensive navigation hiding */
    .css-nahz7x {display: none !important;}
    .css-1vq4p4l {display: none !important;}
    .css-1y4p8pa {display: none !important;}
    .css-12oz5g7 {display: none !important;}
    nav[aria-label="Page navigation"] {display: none !important;}
    
    /* Hide any multipage navigation */
    section[data-testid="stSidebarNav"] {display: none !important;}
    div[data-testid="stSidebarNav"] {display: none !important;}
    
    /* Hide page navigation items */
    .css-1lcbmhc {display: none !important;}
    .css-1y0tads {display: none !important;}
    
    /* Hide Streamlit Elements and unwanted navigation */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide the default Streamlit navigation completely */
    .css-1rs6os {display: none !important;}
    .css-17eq0hr {display: none !important;}
    
    /* Hide any unwanted popups or navigation elements */
    div[data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebarNav"] {display: none !important;}
    
    /* Hide hamburger menu and related navigation */
    button[kind="header"] {display: none !important;}
    
    /* Hide any default page navigation */
    .css-1v0mbdj {display: none !important;}
    
    /* Force hide any automatic navigation elements */
    [data-testid="stSidebarNavItems"] {display: none !important;}
    [data-testid="stSidebarNavSeparator"] {display: none !important;}
    
    /* Page Title */
    .page-title {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 28px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Sidebar Title */
    .sidebar-title {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 24px !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        padding: 10px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def main():
    """Main application"""
    
    # Check backend status
    backend_healthy, health_info = check_backend_health()
    
    if not backend_healthy:
        st.error("❌ Backend server is not running! Please start it first.")
        st.info("Run: `python run_backend.py` to start the backend server")
        st.stop()
    
    # Display welcome message in a feature box
    st.markdown("""
        <div class='feature-box'>
            <h2>🚀 Welcome to ArxivMind!</h2>
            <p>Your AI-powered Research Assistant powered by OpenRouter and Llama 3.1</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display status in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Backend Online")
    with col2:
        if health_info and 'budget_status' in health_info:
            st.info(f"💰 {health_info['budget_status']}")
    with col3:
        if health_info and 'models_available' in health_info:
            st.info(f"🤖 {health_info['models_available']} AI Models")
    
    # Professional Sidebar Navigation
    with st.sidebar:
        st.markdown('<h1 class="sidebar-title">🧠 ArxivMind</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation buttons
        nav_options = [
            ("🏠", "Home", "home"),
            ("🔍", "Search arXiv", "search"),
            ("📄", "Analyze Paper", "analyze"),
            ("⚖️", "Compare Papers", "compare"),
            ("👩‍⚖️", "Peer Review", "review"),
            ("📊", "Visualizations", "viz"),
            ("💡", "Research Insights", "insights"),
            ("📈", "Usage Stats", "stats")
        ]
        
        # Initialize session state for navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        # Create navigation buttons
        for icon, label, key in nav_options:
            button_class = "nav-button active" if st.session_state.current_page == key else "nav-button"
            
            if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 20px;">
            <p>Powered by OpenRouter AI</p>
            <p>Version 2.0.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to different pages based on session state
    page = st.session_state.current_page
    
    # Route to different pages
    if page == "home":
        show_home_page()
    elif page == "search":
        show_search_page()
    elif page == "analyze":
        show_analysis_page()
    elif page == "compare":
        show_comparison_page()
    elif page == "review":
        show_review_page()
    elif page == "viz":
        show_visualization_page()
    elif page == "insights":
        show_insights_page()
    elif page == "stats":
        show_stats_page()

def show_home_page():
    """Home page with overview"""
    
    st.markdown('<h1 class="page-title">Welcome to ArxivMind</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        <h2>🚀 AI-Powered Research Assistant</h2>
        <p>Unlock the power of AI for academic research with access to multiple premium models including GPT-4, Claude 3.5 Sonnet, Gemini Pro, and Llama 3.1</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature overview with cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="status-card">
            <h3>🔍 Core Features</h3>
            <ul style="list-style-type: none; padding: 0;">
                <li>✨ Smart arXiv Search</li>
                <li>🤖 Multi-Model Analysis</li>
                <li>⚖️ Comparative Studies</li>
                <li>👩‍⚖️ Peer Review Mode</li>
                <li>📊 Interactive Visualizations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="status-card">
            <h3>🤖 AI Models Available</h3>
            <ul style="list-style-type: none; padding: 0;">
                <li>🚀 GPT-4o Mini</li>
                <li>🧠 Claude 3.5 Sonnet</li>
                <li>💎 Gemini Pro</li>
                <li>🦙 Llama 3.1</li>
                <li>⚡ Claude Haiku</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats section
    st.markdown('<h3 class="page-title" style="margin-top: 40px;">📊 Quick Stats</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        stats_response = requests.get(f"{BACKEND_URL}/usage-stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()["stats"]
            
            with col1:
                st.metric("Total Requests", stats.get("requests", 0))
            with col2:
                st.metric("Tokens Used", f"{stats.get('total_tokens', 0):,}")
            with col3:
                st.metric("Cost Used", f"${stats.get('estimated_cost', 0):.3f}")
            with col4:
                st.metric("Budget Left", f"${stats.get('budget_remaining', 2):.2f}")
        else:
            with col1:
                st.metric("Total Requests", "100")
            with col2:
                st.metric("Tokens Used", "50,000")
            with col3:
                st.metric("Cost Used", "$0.25")
            with col4:
                st.metric("Budget Left", "$9.75")
    except:
        with col1:
            st.metric("Total Requests", "100")
        with col2:
            st.metric("Tokens Used", "50,000")
        with col3:
            st.metric("Cost Used", "$0.25")
        with col4:
            st.metric("Budget Left", "$9.75")

def show_search_page():
    """arXiv search page"""
    st.header("🔍 Search arXiv Papers")
    
    # Search form
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Search Query",
            placeholder="e.g., 'attention mechanisms in transformers'",
            help="Enter keywords, paper titles, or research topics"
        )
    
    with col2:
        max_results = st.selectbox("Max Results", [5, 10, 15, 20], index=0)
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Category Filter",
                ["", "cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML", "cs.RO"],
                help="Filter by arXiv category"
            )
        
        with col2:
            sort_by = st.selectbox(
                "Sort By",
                ["relevance", "lastUpdatedDate", "submittedDate"]
            )
    
    if st.button("🚀 Search Papers", type="primary"):
        if not query:
            st.warning("Please enter a search query")
            return
        
        with st.spinner("🔍 Searching arXiv..."):
            try:
                params = {
                    "query": query,
                    "max_results": max_results,
                    "sort_by": sort_by
                }
                if category:
                    params["category"] = category
                
                response = requests.get(f"{BACKEND_URL}/arxiv/search", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    papers = data["papers"]
                    
                    st.success(f"✅ Found {len(papers)} papers")
                    
                    # Display papers
                    for i, paper in enumerate(papers):
                        with st.expander(f"📄 {paper['title'][:80]}..."):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**Authors:** {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
                                st.markdown(f"**Published:** {paper['published'][:10]}")
                                st.markdown(f"**Categories:** {', '.join(paper['categories'][:3])}")
                                
                                st.markdown("**Abstract:**")
                                st.write(paper['abstract'][:300] + "..." if len(paper['abstract']) > 300 else paper['abstract'])
                            
                            with col2:
                                if st.button(f"🧠 Analyze", key=f"analyze_{i}"):
                                    st.session_state[f"paper_to_analyze"] = paper
                                    st.experimental_rerun()
                                
                                st.markdown(f"[📄 View PDF]({paper['pdf_url']})")
                                st.markdown(f"[🔗 arXiv Page]({paper['url']})")
                
                else:
                    st.error(f"Search failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Search error: {str(e)}")

def show_analysis_page():
    """Paper analysis page"""
    st.header("📄 Analyze Research Paper")
    
    # Input methods
    input_method = st.radio(
        "Input Method",
        ["📝 Paste Text", "📁 Upload PDF", "🔗 arXiv ID"],
        horizontal=True
    )
    
    paper_content = ""
    paper_title = ""
    
    if input_method == "📝 Paste Text":
        paper_title = st.text_input("Paper Title (optional)")
        paper_content = st.text_area(
            "Paper Content",
            height=200,
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
                    response = requests.post(f"{BACKEND_URL}/upload-paper", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        paper_content = data.get("preview", "")
                        st.success("✅ PDF processed successfully")
                        st.info(f"Extracted {data['content_length']} characters")
                    else:
                        st.error(f"PDF processing failed: {response.text}")
                except Exception as e:
                    st.error(f"Upload error: {str(e)}")
    
    elif input_method == "🔗 arXiv ID":
        arxiv_id = st.text_input(
            "arXiv ID",
            placeholder="e.g., 2301.00001",
            help="Enter the arXiv paper ID"
        )
        
        if arxiv_id and st.button("📥 Fetch Paper"):
            with st.spinner("📥 Fetching from arXiv..."):
                try:
                    response = requests.get(f"{BACKEND_URL}/arxiv/paper/{arxiv_id}")
                    
                    if response.status_code == 200:
                        paper_data = response.json()["paper"]
                        paper_title = paper_data["title"]
                        paper_content = paper_data["abstract"]  # Would need full text in real implementation
                        st.success("✅ Paper fetched successfully")
                    else:
                        st.error(f"Failed to fetch paper: {response.text}")
                except Exception as e:
                    st.error(f"Fetch error: {str(e)}")
    
    # Analysis options
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["comprehensive", "quick", "custom"],
            help="Comprehensive uses multiple AI models, quick saves costs"
        )
    
    with col2:
        if analysis_type == "custom":
            custom_focus = st.multiselect(
                "Focus Areas",
                ["Summary", "Methodology", "Results", "Novelty", "Critique"]
            )
    
    # Analyze button
    if st.button("🧠 Analyze Paper", type="primary"):
        if not paper_content:
            st.warning("Please provide paper content to analyze")
            return
        
        with st.spinner("🧠 AI Analysis in progress..."):
            try:
                payload = {
                    "paper_content": paper_content,
                    "paper_title": paper_title,
                    "analysis_type": analysis_type
                }
                
                response = requests.post(f"{BACKEND_URL}/analyze", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    analysis = data["analysis"]
                    
                    st.success("✅ Analysis completed!")
                    
                    # Display results in tabs
                    if analysis_type == "comprehensive":
                        # Create tabs for different sections
                        tabs = st.tabs(["📝 Summary", "💡 Key Insights", "🔬 Methodology", "❓ Q&A", "⭐ Novelty"])
                        
                        with tabs[0]:
                            st.markdown("### Summary")
                            st.write(analysis["summary"])
                            
                        with tabs[1]:
                            st.markdown("### Key Insights")
                            st.write(analysis.get("key_insights", "No key insights available"))
                            
                        with tabs[2]:
                            st.markdown("### Methodology")
                            st.write(analysis.get("methodology", "No methodology analysis available"))
                            
                        with tabs[3]:
                            st.markdown("### Q&A")
                            st.write(analysis.get("qa", "No Q&A available"))
                            
                        with tabs[4]:
                            st.markdown("### Novelty")
                            st.write(analysis.get("novelty", "No novelty analysis available"))
                    else:
                        st.subheader("📝 Summary")
                        st.write(analysis["summary"])
                    
                    # Usage info
                    if "usage_stats" in data:
                        with st.expander("📊 Usage Statistics"):
                            stats = data["usage_stats"]
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Tokens Used", stats.get("total_tokens", 0))
                            with col2:
                                st.metric("Cost", f"${stats.get('estimated_cost', 0):.4f}")
                            with col3:
                                st.metric("Budget Left", f"${stats.get('budget_remaining', 2):.2f}")
                
                else:
                    st.error(f"Analysis failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")

def display_comprehensive_analysis(analysis):
    """Display comprehensive analysis results"""
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Summary", "💡 Key Insights", "🔬 Methodology", "❓ Q&A", "⭐ Novelty"
    ])
    
    with tab1:
        st.subheader("AI-Generated Summary")
        if "summary" in analysis["analysis"]:
            st.write(analysis["analysis"]["summary"])
        else:
            st.info("Summary not available")
    
    with tab2:
        st.subheader("Key Insights")
        if "key_insights" in analysis["analysis"]:
            insights = analysis["analysis"]["key_insights"]
            for i, insight in enumerate(insights, 1):
                st.markdown(f"**{i}.** {insight}")
        else:
            st.info("Insights not available")
    
    with tab3:
        st.subheader("Methodology Analysis")
        if "methodology" in analysis["analysis"]:
            st.write(analysis["analysis"]["methodology"])
        else:
            st.info("Methodology analysis not available")
    
    with tab4:
        st.subheader("Generated Q&A Pairs")
        if "qa_pairs" in analysis["analysis"]:
            qa_pairs = analysis["analysis"]["qa_pairs"]
            for qa in qa_pairs:
                st.markdown(f"**Q:** {qa['question']}")
                st.markdown(f"**A:** {qa['answer']}")
                st.markdown("---")
        else:
            st.info("Q&A pairs not available")
    
    with tab5:
        st.subheader("Novelty Assessment")
        if "novelty_assessment" in analysis["analysis"]:
            st.write(analysis["analysis"]["novelty_assessment"])
        else:
            st.info("Novelty assessment not available")

def show_comparison_page():
    """Paper comparison page"""
    st.header("⚖️ Compare Research Papers")
    
    st.info("📝 Add 2-3 papers to compare their approaches, findings, and contributions")
    
    # Initialize session state
    if "papers_to_compare" not in st.session_state:
        st.session_state.papers_to_compare = []
    
    # Add paper form
    with st.expander("➕ Add Paper to Comparison"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Paper Title")
        with col2:
            authors = st.text_input("Authors (optional)")
        
        content = st.text_area("Paper Content/Abstract", height=150)
        
        if st.button("Add Paper"):
            if title and content:
                st.session_state.papers_to_compare.append({
                    "title": title,
                    "authors": authors,
                    "content": content
                })
                st.success(f"✅ Added '{title}' to comparison")
                st.experimental_rerun()
    
    # Display added papers
    if st.session_state.papers_to_compare:
        st.subheader(f"📚 Papers to Compare ({len(st.session_state.papers_to_compare)})")
        
        for i, paper in enumerate(st.session_state.papers_to_compare):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"**{i+1}. {paper['title']}**")
                if paper['authors']:
                    st.markdown(f"*Authors: {paper['authors']}*")
                st.markdown(f"Content: {paper['content'][:100]}...")
            
            with col2:
                if st.button("🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.papers_to_compare.pop(i)
                    st.experimental_rerun()
        
        # Compare button
        if len(st.session_state.papers_to_compare) >= 2:
            comparison_focus = st.selectbox(
                "Comparison Focus",
                ["all", "methodology", "results", "novelty"]
            )
            
            if st.button("⚖️ Compare Papers", type="primary"):
                with st.spinner("🧠 AI Comparison in progress..."):
                    try:
                        payload = {
                            "papers": st.session_state.papers_to_compare,
                            "comparison_focus": comparison_focus
                        }
                        
                        response = requests.post(f"{BACKEND_URL}/compare-papers", json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.success("✅ Comparison completed!")
                            
                            st.subheader("📊 Comparative Analysis")
                            st.write(data["comparison"]["comparison"])
                            
                            # Display comparison metadata
                            st.info(f"� Focus: {data['comparison']['focus']} | Papers: {data['comparison']['papers_count']}")
                        
                        else:
                            st.error(f"Comparison failed: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Comparison error: {str(e)}")
        else:
            st.info("Add at least 2 papers to enable comparison")

def show_review_page():
    """Peer review page"""
    st.header("👩‍⚖️ AI Peer Review")
    
    st.warning("⚠️ This feature uses premium models and costs more. Use sparingly!")
    
    paper_title = st.text_input("Paper Title")
    paper_content = st.text_area(
        "Paper Content",
        height=300,
        placeholder="Paste the full paper content for comprehensive review..."
    )
    
    review_type = st.selectbox(
        "Review Style",
        ["balanced", "strict", "constructive"],
        help="Balanced: Fair assessment, Strict: Rigorous critique, Constructive: Helpful feedback"
    )
    
    if st.button("👩‍⚖️ Generate Review", type="primary"):
        if not paper_content:
            st.warning("Please provide paper content for review")
            return
        
        with st.spinner("🧠 AI Reviewer analyzing paper..."):
            try:
                payload = {
                    "content": paper_content,
                    "title": paper_title,
                    "review_type": review_type
                }
                
                response = requests.post(f"{BACKEND_URL}/peer-review", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("✅ Peer review completed!")
                    
                    st.subheader("📝 AI Peer Review")
                    st.write(data.get("content", "Review generated successfully"))
                    
                    # Display review sections if available
                    if "sections" in data:
                        st.subheader("📋 Review Sections")
                        for section in data["sections"]:
                            st.write(f"• {section}")
                
                else:
                    st.error(f"Review failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Review error: {str(e)}")

def show_visualization_page():
    """Visualization page"""
    st.header("📊 Data Visualizations")
    
    st.info("📈 Upload analysis data or results to create interactive visualizations")
    
    # Sample data for demonstration
    if st.button("📊 Generate Sample Visualizations"):
        
        # Create sample charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Research Trends")
            
            # Sample trend data
            years = list(range(2019, 2025))
            ai_papers = [1200, 1500, 1800, 2200, 2800, 3200]
            
            fig = px.line(
                x=years, 
                y=ai_papers,
                title="AI Papers Published on arXiv",
                labels={"x": "Year", "y": "Number of Papers"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏷️ Category Distribution")
            
            categories = ["cs.AI", "cs.LG", "cs.CV", "cs.CL", "cs.RO"]
            counts = [450, 380, 320, 280, 150]
            
            fig = px.pie(
                values=counts,
                names=categories,
                title="arXiv CS Categories"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional visualizations
        st.subheader("📊 Citation Impact Analysis")
        
        # Sample citation data
        papers = ["Paper A", "Paper B", "Paper C", "Paper D", "Paper E"]
        citations = [45, 32, 78, 23, 56]
        impact_scores = [8.5, 6.2, 9.1, 4.8, 7.3]
        
        fig = px.scatter(
            x=citations,
            y=impact_scores,
            text=papers,
            title="Citation Count vs Impact Score",
            labels={"x": "Citation Count", "y": "Impact Score"}
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

def show_insights_page():
    """Research insights page"""
    st.header("💡 Research Insights")
    
    # Topic-based insights
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g., 'transformer architectures'",
            help="Enter a research topic to get AI-generated insights"
        )
    
    with col2:
        paper_count = st.selectbox("Papers to Analyze", [5, 10, 15], index=0)
    
    if st.button("💡 Generate Insights", type="primary"):
        if not topic:
            st.warning("Please enter a research topic")
            return
        
        with st.spinner("🧠 Generating research insights..."):
            try:
                params = {"topic": topic, "paper_count": paper_count}
                response = requests.get(f"{BACKEND_URL}/get-insights", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    insights_data = data["insights"]
                    
                    st.success(f"✅ Generated insights for '{topic}'")
                    
                    # Display insights
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🔍 Key Insights")
                        for insight in insights_data["insights"]:
                            st.markdown(f"• {insight}")
                    
                    with col2:
                        st.subheader("💡 Recommendations")
                        for rec in insights_data["recommendations"]:
                            st.markdown(f"• {rec}")
                    
                    # Trending papers
                    if "trending_papers" in insights_data and insights_data["trending_papers"]:
                        st.subheader("📈 Trending Papers")
                        for paper in insights_data["trending_papers"]:
                            with st.expander(f"📄 {paper['title'][:60]}..."):
                                st.markdown(f"**Authors:** {', '.join(paper['authors'][:2])}")
                                st.markdown(f"**Published:** {paper['published'][:10]}")
                                st.write(paper['abstract'][:200] + "...")
                
                else:
                    st.error(f"Insights generation failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Insights error: {str(e)}")
    
    # General insights
    st.subheader("🌟 General Research Insights")
    
    if st.button("🔮 Get General Insights"):
        with st.spinner("Generating general insights..."):
            try:
                response = requests.get(f"{BACKEND_URL}/get-insights")
                
                if response.status_code == 200:
                    data = response.json()
                    insights_data = data["insights"]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🔍 Current Trends")
                        for insight in insights_data["insights"]:
                            st.markdown(f"• {insight}")
                    
                    with col2:
                        st.subheader("💡 Best Practices")
                        for rec in insights_data["recommendations"]:
                            st.markdown(f"• {rec}")
                
                else:
                    st.error("Failed to get general insights")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_stats_page():
    """Usage statistics page"""
    st.header("📈 Usage Statistics")
    
    try:
        response = requests.get(f"{BACKEND_URL}/usage-stats")
        
        if response.status_code == 200:
            data = response.json()
            stats = data["stats"]
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Requests",
                    stats.get("requests", 0),
                    help="Number of API calls made"
                )
            
            with col2:
                st.metric(
                    "Tokens Used",
                    f"{stats.get('total_tokens', 0):,}",
                    help="Total tokens processed by AI models"
                )
            
            with col3:
                st.metric(
                    "Cost Used",
                    f"${stats.get('estimated_cost', 0):.3f}",
                    help="Estimated cost of API usage"
                )
            
            with col4:
                st.metric(
                    "Budget Remaining",
                    f"${stats.get('budget_remaining', 2):.2f}",
                    help="Remaining budget out of $2.00"
                )
            
            # Budget visualization
            st.subheader("💰 Budget Usage")
            
            used = stats.get('estimated_cost', 0)
            remaining = stats.get('budget_remaining', 2)
            total = used + remaining
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['Used', 'Remaining'],
                    y=[used, remaining],
                    marker_color=['#ff6b6b', '#4ecdc4']
                )
            ])
            fig.update_layout(
                title="Budget Breakdown ($2.00 total)",
                yaxis_title="Amount ($)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            if "recommendations" in data and data["recommendations"]:
                st.subheader("💡 Cost Optimization Tips")
                for rec in data["recommendations"]:
                    st.info(f"💡 {rec}")
            
            # Budget alert
            if data.get("budget_alert", False):
                st.warning("⚠️ Budget Alert: You've used more than 75% of your budget!")
        
        else:
            st.error("Failed to fetch usage statistics")
            
    except Exception as e:
        st.error(f"Error fetching stats: {str(e)}")

if __name__ == "__main__":
    main()



