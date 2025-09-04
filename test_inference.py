#!/usr/bin/env python3
"""
Test Hugging Face Inference API with different models
"""
import os
import requests
import json

# Get token from environment variable
HF_TOKEN = os.environ.get('HF_TOKEN')
print(f"🔑 Using token: {HF_TOKEN[:10]}...")

# Test different models
models_to_test = [
    "gpt2",
    "microsoft/DialoGPT-medium", 
    "facebook/bart-large-cnn",
    "distilbert-base-uncased"
]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

for model in models_to_test:
    print(f"\n🧠 Testing model: {model}")
    print("-" * 40)
    
    # Test 1: Check if model is accessible
    try:
        response = requests.get(f"https://api-inference.huggingface.co/models/{model}", headers=headers)
        print(f"📊 Model Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Model accessible!")
            
            # Test 2: Try inference
            if "text-generation" in model or "gpt" in model.lower():
                payload = {"inputs": "Hello, how are you?"}
            elif "bart" in model.lower():
                payload = {"inputs": "This is a test sentence for summarization."}
            else:
                payload = {"inputs": "This is a test input."}
                
            print(f"📝 Testing inference with: {payload['inputs']}")
            
            inference_response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"🤖 Inference Status: {inference_response.status_code}")
            
            if inference_response.status_code == 200:
                result = inference_response.json()
                print("✅ Inference successful!")
                print(f"   Result: {json.dumps(result, indent=2)[:200]}...")
            elif inference_response.status_code == 503:
                print("⚠️  Model is loading (normal for first request)")
            else:
                print(f"❌ Inference failed: {inference_response.text[:100]}...")
                
        else:
            print(f"❌ Model not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing {model}: {e}")
    
    print()
