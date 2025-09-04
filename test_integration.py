#!/usr/bin/env python3
"""
Test ArxivMind Frontend-Backend Integration
"""
import requests
import time

def test_integration():
    print("🧠 Testing ArxivMind Frontend-Backend Integration...")
    print("=" * 60)
    
    # Test 1: Backend Health
    print("\n1️⃣ Testing Backend Health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running: python run_backend.py")
        return False
    
    # Test 2: Backend API Endpoints
    print("\n2️⃣ Testing Backend API Endpoints...")
    endpoints = [
        ("/", "Root endpoint"),
        ("/docs", "API documentation"),
        ("/get-insights", "Insights endpoint")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {description}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description}: {e}")
    
    # Test 3: Paper Analysis Endpoint
    print("\n3️⃣ Testing Paper Analysis Endpoint...")
    sample_paper = "This is a test research paper about machine learning and artificial intelligence."
    
    try:
        response = requests.post(
            "http://localhost:8000/analyze-paper",
            params={"paper_content": sample_paper},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Paper analysis endpoint working!")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"   Summary: {len(analysis.get('summary', ''))} chars")
                print(f"   Key points: {len(analysis.get('key_points', []))} items")
        else:
            print(f"❌ Paper analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Paper analysis error: {e}")
    
    # Test 4: Frontend Port Check
    print("\n4️⃣ Testing Frontend Port Availability...")
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        print("✅ Frontend port 8501 is accessible!")
    except:
        print("ℹ️  Frontend not running yet (this is normal)")
        print("   Start frontend with: streamlit run arxivmind/app.py --server.port 8501")
    
    print("\n" + "=" * 60)
    print("🎉 Integration Test Completed!")
    print("\n📋 Next Steps:")
    print("   1. Backend is running on: http://localhost:8000")
    print("   2. API docs: http://localhost:8000/docs")
    print("   3. Start frontend: streamlit run arxivmind/app.py --server.port 8501")
    print("   4. Or use: start_arxivmind.bat (starts both)")
    
    return True

if __name__ == "__main__":
    test_integration()
