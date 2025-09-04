#!/usr/bin/env python3
"""
Test ArxivMind Backend
Simple test script to verify backend functionality
"""

import requests
import json
import time

def test_backend():
    """Test the backend endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ArxivMind Backend...")
    print("=" * 40)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Available endpoints: {len(data.get('endpoints', {}))}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: API documentation
    print("\n3️⃣ Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible!")
            print(f"   Visit: {base_url}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Backend test completed!")
    print(f"🌐 Backend URL: {base_url}")
    print(f"📖 API Docs: {base_url}/docs")
    print(f"🔍 Health: {base_url}/health")
    
    return True

def test_with_sample_data():
    """Test backend with sample data"""
    
    base_url = "http://localhost:8000"
    
    print("\n🧪 Testing with sample data...")
    print("=" * 40)
    
    # Sample paper content
    sample_content = """
    This is a sample research paper about artificial intelligence and machine learning.
    The paper discusses various approaches to natural language processing and their applications.
    The methodology involves deep learning techniques and neural network architectures.
    Results show significant improvements in text classification tasks.
    Future work should focus on improving efficiency and reducing computational costs.
    """
    
    # Test paper analysis
    print("\n📝 Testing paper analysis...")
    try:
        response = requests.post(
            f"{base_url}/analyze-paper",
            json={"paper_content": sample_content}
        )
        
        if response.status_code == 200:
            print("✅ Paper analysis working!")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Paper analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Paper analysis error: {e}")
    
    # Test insights generation
    print("\n💡 Testing insights generation...")
    try:
        response = requests.get(f"{base_url}/get-insights")
        
        if response.status_code == 200:
            print("✅ Insights generation working!")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
            insights = data.get('insights', {}).get('insights', [])
            print(f"   Generated {len(insights)} insights")
        else:
            print(f"❌ Insights generation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Insights generation error: {e}")

if __name__ == "__main__":
    print("🚀 ArxivMind Backend Test Suite")
    print("Make sure the backend is running before running this test!")
    print()
    
    # Wait a moment for user to read
    input("Press Enter to start testing...")
    
    # Test basic functionality
    if test_backend():
        # Test with sample data
        test_with_sample_data()
    
    print("\n✨ Test completed! Check the results above.")
