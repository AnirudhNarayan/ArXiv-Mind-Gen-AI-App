#!/usr/bin/env python3
"""
Test OpenRouter API Access
Check what models you can access with your API key
"""
import requests
import json

# Your OpenRouter API key from the email
OPENROUTER_API_KEY = "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"

def test_openrouter_access():
    print("🚀 Testing OpenRouter API Access...")
    print("=" * 50)
    
    # Test 1: List available models
    print("\n1️⃣ Fetching available models...")
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://arxivmind.com",
                "X-Title": "ArxivMind"
            }
        )
        
        if response.status_code == 200:
            models_data = response.json()
            print("✅ Successfully fetched models!")
            print(f"   Total models available: {len(models_data.get('data', []))}")
            
            # Show top models by category
            print("\n📋 Top Models by Category:")
            
            # Group models by provider
            providers = {}
            for model in models_data.get('data', []):
                provider = model.get('id', '').split('/')[0] if '/' in model.get('id', '') else 'Other'
                if provider not in providers:
                    providers[provider] = []
                providers[provider].append({
                    'id': model.get('id'),
                    'name': model.get('name', 'Unknown'),
                    'context_length': model.get('context_length', 0),
                    'pricing': model.get('pricing', {})
                })
            
            # Show top providers
            for provider, models in list(providers.items())[:8]:  # Top 8 providers
                print(f"\n   🔹 {provider.upper()}:")
                for model in models[:3]:  # Top 3 models per provider
                    pricing = model.get('pricing', {})
                    input_cost = pricing.get('input', 'N/A')
                    output_cost = pricing.get('output', 'N/A')
                    print(f"      • {model['id']} (Context: {model['context_length']:,})")
                    print(f"        💰 Input: ${input_cost}/1K tokens, Output: ${output_cost}/1K tokens")
            
        else:
            print(f"❌ Failed to fetch models: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error fetching models: {e}")
    
    # Test 2: Test a simple chat completion
    print("\n2️⃣ Testing chat completion...")
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://arxivmind.com",
                "X-Title": "ArxivMind"
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # Start with a reliable model
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello! Can you give me a brief summary of what OpenRouter is?"
                    }
                ],
                "max_tokens": 100
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat completion successful!")
            print(f"   Model used: {result.get('model', 'Unknown')}")
            print(f"   Response: {result['choices'][0]['message']['content']}")
            
            # Show usage info
            if 'usage' in result:
                usage = result['usage']
                print(f"   Tokens used: {usage.get('total_tokens', 0)}")
                print(f"   Input tokens: {usage.get('prompt_tokens', 0)}")
                print(f"   Output tokens: {usage.get('completion_tokens', 0)}")
                
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error in chat completion: {e}")
    
    # Test 3: Check your credits
    print("\n3️⃣ Checking your credits...")
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            }
        )
        
        if response.status_code == 200:
            key_info = response.json()
            print("✅ Credit info retrieved!")
            print(f"   Credits remaining: ${key_info.get('credits', 'N/A')}")
            print(f"   Key name: {key_info.get('name', 'N/A')}")
            print(f"   Created: {key_info.get('created_at', 'N/A')}")
        else:
            print(f"❌ Failed to get credit info: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting credit info: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 OpenRouter Test Completed!")
    print("\n💡 Next Steps:")
    print("   1. You now have access to hundreds of AI models!")
    print("   2. We can integrate this into your ArxivMind backend")
    print("   3. Much more powerful than the previous Hugging Face setup")
    print("   4. Use your $10 credit wisely!")

if __name__ == "__main__":
    test_openrouter_access()
