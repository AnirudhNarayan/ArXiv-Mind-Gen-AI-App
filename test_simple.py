#!/usr/bin/env python3
"""
Simple Hugging Face Test - Following Official Documentation
"""
import os
import requests
import json

# Get token from environment variable
HF_TOKEN = os.environ.get('HF_TOKEN')
print(f"🔑 Using token: {HF_TOKEN[:10]}...")

# Following the documentation exactly
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
payload = {"inputs": "The Eiffel Tower is in"}

print(f"\n🚀 Testing with model: distilgpt2")
print(f"📝 Input: 'The Eiffel Tower is in'")

try:
    r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    print(f"📊 Status Code: {r.status_code}")
    
    if r.status_code == 200:
        print("✅ SUCCESS! Model inference working!")
        result = r.json()
        print(f"🤖 Generated text: {json.dumps(result, indent=2)}")
    elif r.status_code == 503:
        print("⚠️  Model is loading (this is normal for first request)")
    else:
        print(f"❌ Failed: {r.status_code}")
        print(f"📄 Response: {r.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
