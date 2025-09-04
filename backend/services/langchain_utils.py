"""
Minimal LangChain utilities for ArxivMind
"""
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

def enhance_paper_analysis(content: str, metadata: Dict[str, Any]) -> str:
    """Enhance paper analysis using LangChain text splitting"""
    try:
        # Create text splitter for better chunk management
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )
        
        # Split content into manageable chunks
        chunks = text_splitter.split_text(content)
        
        # Create a summarization prompt
        prompt = PromptTemplate(
            template="""Analyze this section of a research paper:
            
            {text}
            
            Focus on:
            1. Key findings and contributions
            2. Novel technical aspects
            3. Methodology insights
            
            Analysis:""",
            input_variables=["text"]
        )
        
        # For now, just return the structured chunks
        enhanced_content = "\n\n".join([
            f"Section {i+1}:\n{chunk}" 
            for i, chunk in enumerate(chunks[:3])  # Just first 3 chunks
        ])
        
        return enhanced_content
        
    except Exception as e:
        return f"Enhancement failed: {str(e)}"
