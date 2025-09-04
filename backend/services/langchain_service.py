#!/usr/bin/env python3
"""
LangChain Integration Service for ArxivMind
This service provides enhanced document processing and analysis using LangChain.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, List, Any, Optional
import logging
import os

logger = logging.getLogger(__name__)

class LangChainService:
    """Enhanced document processing using LangChain"""
    
    def __init__(self, openrouter_key: str):
        """Initialize LangChain service with OpenRouter key"""
        self.openrouter_key = openrouter_key
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Initialize embeddings and LLM
        self.embeddings = OpenAIEmbeddings(openai_api_key=openrouter_key)
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=openrouter_key
        )
        
        # Initialize prompts
        self.summary_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""Based on the following paper content:
            {context}
            
            Please provide a detailed response to: {question}
            Focus on being comprehensive yet concise.
            """
        )
        
        logger.info("LangChain service initialized")
    
    async def process_paper(self, content: str) -> Dict[str, Any]:
        """Process paper using LangChain for enhanced analysis"""
        try:
            # Split text into chunks
            texts = self.text_splitter.split_text(content)
            
            # Create vector store
            vectorstore = Chroma.from_texts(
                texts,
                self.embeddings,
                metadatas=[{"source": f"chunk_{i}"} for i in range(len(texts))]
            )
            
            # Create retrieval chain
            retriever = vectorstore.as_retriever(
                search_type="mmr",  # Maximum Marginal Relevance
                search_kwargs={"k": 3}
            )
            
            # Create chains for different aspects
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            
            summary_chain = LLMChain(
                llm=self.llm,
                prompt=self.summary_prompt
            )
            
            # Get enhanced analysis
            summary = await self._get_enhanced_summary(content, summary_chain)
            novelty = await self._get_novelty_analysis(content, qa_chain)
            
            return {
                "enhanced_summary": summary,
                "enhanced_novelty": novelty,
                "processing_info": {
                    "chunks_processed": len(texts),
                    "using_langchain": True
                }
            }
            
        except Exception as e:
            logger.error(f"LangChain processing error: {str(e)}")
            raise
    
    async def _get_enhanced_summary(self, content: str, chain: LLMChain) -> str:
        """Get enhanced summary using LangChain"""
        try:
            response = await chain.arun({
                "context": content[:2000],
                "question": "Provide a detailed summary of this research paper's main points and contributions."
            })
            return response
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}")
            return "Error generating enhanced summary."
    
    async def _get_novelty_analysis(self, content: str, qa_chain: RetrievalQA) -> str:
        """Get novelty analysis using QA chain"""
        try:
            response = await qa_chain.arun(
                "What are the novel and innovative aspects of this research? "
                "How does it advance the state of the art?"
            )
            return response
        except Exception as e:
            logger.error(f"Novelty analysis error: {str(e)}")
            return "Error analyzing novelty."
