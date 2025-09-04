#!/usr/bin/env python3
"""
Test Hugging Face Authentication
"""
import os
import requests

# Get token from environment variable
HF_TOKEN = os.environ.get('HF_TOKEN')
print(f"🔑 Testing token: {HF_TOKEN[:10]}...")

# Test 1: Basic authentication
print("\n1️⃣ Testing basic authentication...")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

try:
    response = requests.get("https://huggingface.co/api/whoami", headers=headers)
    print(f"📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        user_info = response.json()
        print("✅ SUCCESS! Token is working!")
        print(f"   User: {user_info.get('name', 'Unknown')}")
        print(f"   Email: {user_info.get('email', 'Not shown')}")
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Check if we can access model info
print("\n2️⃣ Testing model access...")
try:
    response = requests.get("https://huggingface.co/api/models/distilgpt2", headers=headers)
    print(f"📊 Model Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Can access model info!")
    else:
        print(f"❌ Cannot access model: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
