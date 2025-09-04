#!/usr/bin/env python3
"""
Test Full ArxivMind Backend Functionality
"""
import requests
import json

def test_full_backend():
    print("🧠 Testing Full ArxivMind Backend...")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Paper Analysis
    print("\n1️⃣ Testing Paper Analysis...")
    sample_paper = """
    Title: Advances in Machine Learning for Natural Language Processing
    
    Abstract: This paper presents a comprehensive survey of recent advances in machine learning 
    approaches for natural language processing tasks. We examine the evolution from traditional 
    statistical methods to modern deep learning architectures, including transformers and attention mechanisms.
    
    Introduction: Natural Language Processing (NLP) has witnessed remarkable progress in recent years, 
    driven by advances in machine learning and deep learning. The introduction of transformer 
    architectures has revolutionized the field, enabling unprecedented performance on various NLP tasks.
    
    Methodology: Our study employs a systematic literature review approach, analyzing over 200 
    research papers published between 2018 and 2024. We categorize approaches based on their 
    architectural design, training methodology, and application domains.
    
    Results: The analysis reveals that transformer-based models achieve state-of-the-art 
    performance across most NLP benchmarks. BART, GPT, and their variants demonstrate superior 
    capabilities in understanding context and generating coherent text.
    
    Conclusion: Machine learning continues to drive innovation in NLP, with transformer 
    architectures representing the current state-of-the-art. Future research should focus on 
    improving efficiency, reducing computational costs, and enhancing interpretability.
    """
    
    try:
        response = requests.post(
            f"{base_url}/analyze-paper",
            params={"paper_content": sample_paper},
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Paper analysis successful!")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"   Summary length: {len(analysis.get('summary', ''))} chars")
                print(f"   Key points: {len(analysis.get('key_points', []))} items")
                print(f"   Methodology: {len(analysis.get('methodology', ''))} chars")
        else:
            print(f"❌ Analysis failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
    
    # Test 2: Insights Generation
    print("\n2️⃣ Testing Insights Generation...")
    try:
        response = requests.get(f"{base_url}/get-insights", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Insights generation successful!")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if 'insights' in result:
                insights = result['insights']
                print(f"   Generated {len(insights.get('insights', []))} insights")
                print(f"   Generated {len(insights.get('recommendations', []))} recommendations")
        else:
            print(f"❌ Insights failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Insights error: {e}")
    
    # Test 3: Data Visualization
    print("\n3️⃣ Testing Data Visualization...")
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
    
    try:
        response = requests.post(
            f"{base_url}/visualize-data",
            json=sample_data,
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Visualization successful!")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if 'charts' in result:
                charts = result['charts']
                print(f"   Created {len(charts)} charts")
                for chart_name in charts.keys():
                    print(f"     • {chart_name}")
        else:
            print(f"❌ Visualization failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Visualization error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend Test Completed!")
    print(f"🌐 Backend URL: {base_url}")
    print(f"📖 API Docs: {base_url}/docs")

if __name__ == "__main__":
    test_full_backend()
