import requests

API_KEY = "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"

print("🔍 Checking OpenRouter models...")

try:
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        models = data.get('data', [])
        print(f"✅ Found {len(models)} models!")
        
        # Show first 10 models
        print("\n📋 Available Models:")
        for i, model in enumerate(models[:10]):
            print(f"{i+1}. {model.get('id', 'Unknown')}")
            
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
