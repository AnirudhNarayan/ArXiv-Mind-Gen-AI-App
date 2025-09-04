#!/usr/bin/env python3
"""
Test ArxivMind Backend Status
"""
import requests
import time

def test_backend():
    print("🧠 Testing ArxivMind Backend...")
    print("=" * 40)
    
    try:
        # Test health endpoint
        print("1️⃣ Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Backend is working!")
            
            # Test root endpoint
            print("\n2️⃣ Testing root endpoint...")
            response = requests.get("http://localhost:8000/", timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Message: {data.get('message', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")
            
            # Test API docs
            print("\n3️⃣ Testing API documentation...")
            response = requests.get("http://localhost:8000/docs", timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ API docs accessible!")
                print("   🌐 Visit: http://localhost:8000/docs")
            
        else:
            print("❌ Backend not responding properly")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend on port 8000")
        print("   Backend might not be running")
    except Exception as e:
        print(f"❌ Error testing backend: {e}")

if __name__ == "__main__":
    test_backend()
