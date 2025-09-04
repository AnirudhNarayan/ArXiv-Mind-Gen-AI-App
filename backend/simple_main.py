#!/usr/bin/env python3
"""
Simple ArxivMind Backend API
Simplified FastAPI backend with basic OpenAI integration
"""

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import Optional, Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our simple services
try:
    from .services.pdf_parser import PDFParser
    from .services.simple_ai_analyzer import SimpleAIAnalyzer
except ImportError:
    # For direct execution
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from services.pdf_parser import PDFParser
    from services.simple_ai_analyzer import SimpleAIAnalyzer

app = FastAPI(
    title="ArxivMind Simple API",
    description="Simple AI-powered research paper analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_parser = PDFParser()
ai_analyzer = SimpleAIAnalyzer()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🧠 ArxivMind Simple API",
        "version": "1.0.0",
        "features": [
            "Simple paper analysis",
            "PDF text extraction", 
            "Basic insights generation",
            "Cost-optimized AI calls"
        ],
        "endpoints": {
            "analyze": "/analyze-paper",
            "insights": "/get-insights",
            "health": "/health",
            "usage": "/usage-stats"
        },
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        usage_stats = ai_analyzer.get_usage_stats()
        
        return {
            "status": "healthy",
            "service": "ArxivMind Simple API",
            "budget_remaining": f"${usage_stats['budget_remaining']:.3f}",
            "requests_made": usage_stats['requests'],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/analyze-paper")
async def analyze_paper(
    paper_content: str = Query(..., description="Full text content of the research paper"),
    paper_title: str = Query("", description="Title of the paper (optional)")
):
    """
    Simple AI-powered paper analysis
    """
    try:
        logger.info(f"Starting analysis for paper: {paper_title[:50]}...")
        
        if not paper_content.strip():
            raise HTTPException(status_code=400, detail="Paper content cannot be empty")
        
        # Analyze paper
        analysis = ai_analyzer.analyze_paper_simple(paper_content, paper_title)
        
        return {
            "message": "Paper analysis completed successfully",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/get-insights")
async def get_insights(
    paper_content: str = Query(..., description="Paper content for insights generation")
):
    """
    Generate insights from paper content
    """
    try:
        logger.info("Generating insights...")
        
        insights = ai_analyzer.generate_insights(paper_content)
        usage_stats = ai_analyzer.get_usage_stats()
        
        return {
            "message": "Insights generated successfully",
            "insights": insights,
            "usage_stats": usage_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Insights error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

@app.get("/usage-stats")
async def get_usage_statistics():
    """Get current API usage statistics"""
    try:
        stats = ai_analyzer.get_usage_stats()
        
        return {
            "message": "Usage statistics retrieved",
            "stats": stats,
            "budget_alert": stats["estimated_cost"] > 1.0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


