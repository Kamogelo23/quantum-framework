"""
Direct test of Gemini API to diagnose the issue
"""
import requests
import json

API_KEY = 'AIzaSyA-iT2RJh7EkJXHB-yMxWMANxvN0RuOCQU'

# Try different endpoints
endpoints = [
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}",
    f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}",
    f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={API_KEY}",
]

payload = {
    "contents": [{
        "parts": [{"text": "Say hello"}]
    }]
}

print("Testing Gemini API endpoints...")
print("=" * 70)

for i, url in enumerate(endpoints, 1):
    print(f"\n{i}. Testing: {url.split('?')[0]}")
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   SUCCESS! Response: {json.dumps(result, indent=2)[:200]}...")
            print("\n   This endpoint works!")
            break
        else:
            print(f"   Error: {response.text[:200]}")
    except Exception as e:
        print(f"   Exception: {str(e)[:200]}")

print("\n" + "=" * 70)
print("\nIf all endpoints failed, the API key might not be activated.")
print("Visit: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
print("And click 'Enable' to activate the Generative Language API.")
