"""
List available Gemini models for this API key
"""
import requests

API_KEY = 'AIzaSyA-iT2RJh7EkJXHB-yMxWMANxvN0RuOCQU'

# Try to list available models
print("Checking available Gemini models for your API key...")
print("=" * 70)

endpoints = [
    f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}",
    f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}",
]

for endpoint in endpoints:
    print(f"\nTrying: {endpoint.split('?')[0]}")
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            models = response.json()
            print(f"   SUCCESS! Found {len(models.get('models', []))} models:")
            for model in models.get('models', [])[:5]:
                name = model.get('name', 'unknown')
                print(f"   - {name}")
            break
        else:
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)[:200]}")

print("\n" + "=" * 70)
print("\nIf you see 'permission denied' or no models listed,")
print("your API key might be restricted to AI Studio only.")
print("\nSolution: Use Ollama (local, 100% free) instead:")
print("  1. Download: https://ollama.ai/download")
print("  2. Run: ollama pull llama3")
print("  3. Run: ollama serve")
print("  4. Update .env: AI_PROVIDER=ollama")
