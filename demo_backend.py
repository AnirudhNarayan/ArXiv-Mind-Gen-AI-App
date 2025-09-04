#!/usr/bin/env python3
"""
ArxivMind Backend Demo
Demonstrates the backend capabilities with sample data
"""

import asyncio
import json
from pathlib import Path
import sys

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from services.pdf_parser import PDFParser
from services.llm_analyzer import LLMAnalyzer
from services.data_visualizer import DataVisualizer

async def demo_backend():
    """Demonstrate backend capabilities"""
    
    print("🧠 ArxivMind Backend Demo")
    print("=" * 50)
    
    # Initialize services
    pdf_parser = PDFParser()
    llm_analyzer = LLMAnalyzer()
    data_visualizer = DataVisualizer()
    
    # Sample research paper content
    sample_paper = """
    Title: Advances in Machine Learning for Natural Language Processing
    
    Abstract:
    This paper presents a comprehensive survey of recent advances in machine learning 
    approaches for natural language processing tasks. We examine the evolution from 
    traditional statistical methods to modern deep learning architectures, including 
    transformers and attention mechanisms.
    
    Introduction:
    Natural Language Processing (NLP) has witnessed remarkable progress in recent years, 
    driven by advances in machine learning and deep learning. The introduction of 
    transformer architectures has revolutionized the field, enabling unprecedented 
    performance on various NLP tasks.
    
    Methodology:
    Our study employs a systematic literature review approach, analyzing over 200 
    research papers published between 2018 and 2024. We categorize approaches based 
    on their architectural design, training methodology, and application domains.
    
    Results:
    The analysis reveals that transformer-based models achieve state-of-the-art 
    performance across most NLP benchmarks. BERT, GPT, and their variants demonstrate 
    superior capabilities in understanding context and generating coherent text.
    
    Conclusion:
    Machine learning continues to drive innovation in NLP, with transformer 
    architectures representing the current state-of-the-art. Future research should 
    focus on improving efficiency, reducing computational costs, and enhancing 
    interpretability of these models.
    
    References:
    1. Vaswani et al. "Attention Is All You Need" (2017)
    2. Devlin et al. "BERT: Pre-training of Deep Bidirectional Transformers" (2018)
    3. Brown et al. "Language Models are Few-Shot Learners" (2020)
    """
    
    print("\n📄 Sample Research Paper Content:")
    print("-" * 30)
    print(sample_paper[:300] + "...")
    
    # Demo 1: PDF Parser (simulating text extraction)
    print("\n🔍 Demo 1: PDF Text Processing")
    print("-" * 30)
    
    # Extract sections
    sections = pdf_parser.extract_sections(sample_paper)
    print(f"✅ Extracted {len(sections)} sections:")
    for section, content in sections.items():
        if content:
            print(f"   • {section.title()}: {len(content)} characters")
    
    # Extract keywords
    keywords = pdf_parser.extract_keywords(sample_paper, max_keywords=8)
    print(f"\n✅ Top keywords: {', '.join(keywords)}")
    
    # Demo 2: LLM Analysis
    print("\n🤖 Demo 2: AI-Powered Analysis")
    print("-" * 30)
    
    # Check if HF token is available
    if llm_analyzer.hf_token and llm_analyzer.hf_token != "your_huggingface_token_here":
        print("✅ Hugging Face token detected - running AI analysis...")
        
        try:
            analysis = await llm_analyzer.analyze_paper(sample_paper)
            print(f"✅ Analysis completed successfully!")
            print(f"   • Paper length: {analysis['paper_length']} characters")
            print(f"   • Analysis timestamp: {analysis['timestamp']}")
            
            # Show analysis results
            if 'analysis' in analysis:
                for key, value in analysis['analysis'].items():
                    if isinstance(value, list):
                        print(f"   • {key.replace('_', ' ').title()}: {len(value)} items")
                    else:
                        print(f"   • {key.replace('_', ' ').title()}: {len(str(value))} characters")
            
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
    else:
        print("⚠️  No Hugging Face token - skipping AI analysis")
        print("   Set HF_TOKEN environment variable to enable AI features")
    
    # Demo 3: Data Visualization
    print("\n📊 Demo 3: Data Visualization")
    print("-" * 30)
    
    try:
        # Create sample data for visualization
        sample_data = {
            "analysis": {
                "summary": "This paper presents advances in machine learning for NLP",
                "key_points": [
                    "Transformer architectures revolutionize NLP",
                    "BERT and GPT achieve state-of-the-art performance",
                    "Attention mechanisms improve context understanding"
                ],
                "methodology": "Systematic literature review of 200+ papers",
                "results": "Transformers outperform traditional methods"
            },
            "metadata": {
                "word_count": 250,
                "estimated_pages": 3,
                "has_abstract": True,
                "has_references": True,
                "language": "english"
            }
        }
        
        charts = await data_visualizer.create_charts(sample_data)
        print("✅ Visualizations created successfully!")
        
        # Show available chart types
        chart_types = data_visualizer.get_available_chart_types()
        print(f"   • Available chart types: {len(chart_types)}")
        print(f"   • Chart templates: {', '.join(data_visualizer.get_chart_templates())}")
        
        # Show created charts
        if 'charts' in charts:
            for chart_name, chart_data in charts['charts'].items():
                if 'error' not in chart_data:
                    print(f"   • {chart_name}: {chart_data.get('type', 'unknown')} chart")
                else:
                    print(f"   • {chart_name}: {chart_data['error']}")
        
    except Exception as e:
        print(f"❌ Visualization failed: {str(e)}")
    
    # Demo 4: Insights Generation
    print("\n💡 Demo 4: Insights Generation")
    print("-" * 30)
    
    try:
        insights = await llm_analyzer.generate_insights()
        if 'insights' in insights:
            print("✅ Insights generated successfully!")
            print(f"   • Generated {len(insights['insights'])} insights")
            print(f"   • Generated {len(insights['recommendations'])} recommendations")
            
            print("\n   Top insights:")
            for i, insight in enumerate(insights['insights'][:3], 1):
                print(f"   {i}. {insight}")
                
        else:
            print(f"❌ Insights generation failed: {insights.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Insights generation failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend Demo Completed!")
    print("\n🚀 To run the full backend server:")
    print("   python run_backend.py")
    print("\n📖 API Documentation:")
    print("   http://localhost:8000/docs")
    print("\n🧪 Test the backend:")
    print("   python test_backend.py")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_backend())
