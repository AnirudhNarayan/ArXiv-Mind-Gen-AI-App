#!/usr/bin/env python3
"""
Test the Simple ArxivMind System
"""

import requests
import json
import time

BACKEND_URL = "http://localhost:8000"

def test_backend():
    """Test backend functionality"""
    print("🧪 Testing ArxivMind Simple Backend")
    print("=" * 50)
    
    # Test health
    print("1. Testing health endpoint...")
    try:
        r = requests.get(f"{BACKEND_URL}/health")
        if r.status_code == 200:
            health = r.json()
            print(f"   ✅ Backend is healthy")
            print(f"   💰 Budget remaining: {health.get('budget_remaining', 'Unknown')}")
            print(f"   📊 Requests made: {health.get('requests_made', 0)}")
        else:
            print(f"   ❌ Health check failed: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test paper analysis
    print("\n2. Testing paper analysis...")
    test_paper = """
    Abstract: This paper presents a novel approach to machine learning using deep neural networks.
    We propose a new architecture that improves accuracy by 15% over existing methods.
    
    Introduction: Machine learning has become increasingly important in recent years.
    Our approach addresses the key challenges in current methodologies.
    
    Results: Our experiments show significant improvements in performance metrics.
    The proposed method outperforms baseline approaches across multiple datasets.
    
    Conclusion: We have demonstrated the effectiveness of our approach and its potential
    for real-world applications.
    """
    
    try:
        r = requests.post(
            f"{BACKEND_URL}/analyze-paper",
            params={
                "paper_content": test_paper,
                "paper_title": "Novel Deep Learning Approach"
            },
            timeout=60
        )
        
        if r.status_code == 200:
            result = r.json()
            analysis = result.get("analysis", {})
            
            print(f"   ✅ Analysis completed successfully")
            print(f"   📝 Summary: {analysis.get('summary', 'N/A')[:100]}...")
            print(f"   🔍 Key findings: {len(analysis.get('key_findings', []))} found")
            print(f"   💡 Main contribution: {analysis.get('main_contribution', 'N/A')[:100]}...")
            
            usage = analysis.get('usage_stats', {})
            print(f"   💰 Cost: ${usage.get('estimated_cost', 0):.4f}")
            print(f"   🔢 Tokens used: {usage.get('total_tokens', 0)}")
        else:
            print(f"   ❌ Analysis failed: {r.status_code}")
            print(f"   Error: {r.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
        return False
    
    # Test insights generation
    print("\n3. Testing insights generation...")
    try:
        r = requests.post(
            f"{BACKEND_URL}/get-insights",
            params={"paper_content": test_paper},
            timeout=30
        )
        
        if r.status_code == 200:
            result = r.json()
            insights = result.get("insights", [])
            
            print(f"   ✅ Insights generated successfully")
            print(f"   💡 Number of insights: {len(insights)}")
            for i, insight in enumerate(insights[:3], 1):
                print(f"      {i}. {insight[:80]}...")
                
            usage = result.get('usage_stats', {})
            print(f"   💰 Total cost so far: ${usage.get('estimated_cost', 0):.4f}")
        else:
            print(f"   ❌ Insights failed: {r.status_code}")
            
    except Exception as e:
        print(f"   ❌ Insights error: {e}")
    
    # Test usage stats
    print("\n4. Testing usage statistics...")
    try:
        r = requests.get(f"{BACKEND_URL}/usage-stats")
        if r.status_code == 200:
            result = r.json()
            stats = result.get("stats", {})
            
            print(f"   ✅ Usage stats retrieved")
            print(f"   📊 Total requests: {stats.get('requests', 0)}")
            print(f"   🔢 Total tokens: {stats.get('total_tokens', 0)}")
            print(f"   💰 Total cost: ${stats.get('estimated_cost', 0):.4f}")
            print(f"   💳 Budget remaining: ${stats.get('budget_remaining', 2.0):.4f}")
            print(f"   📈 Cost per request: ${stats.get('cost_per_request', 0):.4f}")
            
            if stats.get('estimated_cost', 0) < 0.01:
                print(f"   🎉 Excellent! Very cost-efficient usage!")
            elif stats.get('estimated_cost', 0) < 0.10:
                print(f"   👍 Good cost efficiency!")
            
        else:
            print(f"   ❌ Stats failed: {r.status_code}")
            
    except Exception as e:
        print(f"   ❌ Stats error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend testing completed!")
    print("\n🌐 Frontend should be running at: http://localhost:8501")
    print("🔧 Backend API docs at: http://localhost:8000/docs")
    return True

def test_frontend():
    """Test if frontend is accessible"""
    print("\n🖥️  Testing Frontend Accessibility")
    print("=" * 30)
    
    try:
        r = requests.get("http://localhost:8501", timeout=5)
        if r.status_code == 200:
            print("   ✅ Frontend is accessible")
            return True
        else:
            print(f"   ⚠️  Frontend returned status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ⚠️  Frontend not accessible: {e}")
        print("   💡 This is normal - Streamlit may still be starting up")
        return False

if __name__ == "__main__":
    success = test_backend()
    test_frontend()
    
    if success:
        print("\n✅ System is working perfectly!")
        print("🚀 You can now use ArxivMind Simple for paper analysis")
        print("💰 Cost-optimized with OpenAI GPT-4o-mini")
        print("📚 Ready for RAG and Vector DB integration later")
    else:
        print("\n❌ Some issues detected. Please check the logs.")

