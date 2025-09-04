#!/usr/bin/env python3
"""
PDF Parser Service
Handles PDF text extraction and preprocessing
"""

import PyPDF2
import pdfplumber
from fastapi import UploadFile
import io
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    """Service for parsing PDF research papers"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    async def parse_pdf(self, file: UploadFile) -> str:
        """
        Parse PDF file and extract text content
        
        Args:
            file: Uploaded PDF file
            
        Returns:
            str: Extracted text content
        """
        try:
            # Read file content
            content = await file.read()
            
            # Try multiple parsing methods for better results
            text = await self._extract_text_multiple_methods(content)
            
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            logger.info(f"Successfully parsed PDF: {file.filename}")
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file.filename}: {str(e)}")
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    async def _extract_text_multiple_methods(self, content: bytes) -> str:
        """Extract text using multiple PDF parsing methods"""
        text = ""
        
        # Method 1: PyPDF2
        try:
            text += self._extract_with_pypdf2(content)
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {str(e)}")
        
        # Method 2: pdfplumber (often better for complex layouts)
        try:
            text += self._extract_with_pdfplumber(content)
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
        
        if not text.strip():
            raise Exception("All PDF parsing methods failed")
        
        return text
    
    def _extract_with_pypdf2(self, content: bytes) -> str:
        """Extract text using PyPDF2"""
        text = ""
        pdf_file = io.BytesIO(content)
        
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
                
        except Exception as e:
            logger.warning(f"PyPDF2 extraction error: {str(e)}")
        
        return text
    
    def _extract_with_pdfplumber(self, content: bytes) -> str:
        """Extract text using pdfplumber"""
        text = ""
        pdf_file = io.BytesIO(content)
        
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    if page.extract_text():
                        text += page.extract_text() + "\n"
                        
        except Exception as e:
            logger.warning(f"pdfplumber extraction error: {str(e)}")
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and preprocess extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}]', '', text)
        
        # Clean up multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract common research paper sections
        
        Args:
            text: Full paper text
            
        Returns:
            Dict: Section name -> content mapping
        """
        sections = {}
        
        # Common section patterns
        section_patterns = {
            'abstract': r'(?i)abstract\s*\n(.*?)(?=\n\s*\n|\n\s*introduction|\n\s*1\.)',
            'introduction': r'(?i)introduction\s*\n(.*?)(?=\n\s*\n|\n\s*related work|\n\s*2\.)',
            'methodology': r'(?i)(methodology|methods|approach)\s*\n(.*?)(?=\n\s*\n|\n\s*results|\n\s*3\.)',
            'results': r'(?i)results\s*\n(.*?)(?=\n\s*\n|\n\s*conclusion|\n\s*4\.)',
            'conclusion': r'(?i)conclusion\s*\n(.*?)(?=\n\s*\n|\n\s*references|\n\s*5\.)',
            'references': r'(?i)references?\s*\n(.*?)$'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()
            else:
                sections[section_name] = ""
        
        return sections
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract potential keywords from text
        
        Args:
            text: Paper text
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            List: Extracted keywords
        """
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b\w{4,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'were', 'said',
            'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other', 'than',
            'first', 'then', 'some', 'very', 'when', 'into', 'just', 'more', 'over', 'also'
        }
        
        words = [word for word in words if word not in stop_words]
        
        # Count frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:max_keywords]]
        
        return keywords
