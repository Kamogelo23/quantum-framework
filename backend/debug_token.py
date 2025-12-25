#!/usr/bin/env python
"""Debug script to decode JWT token and check its contents"""
import jwt
import json

# Paste the token from browser console here
TOKEN = input("Paste your access token: ").strip()

# Decode without verification to see contents
try:
    unverified = jwt.decode(TOKEN, options={"verify_signature": False})
    print("\n=== TOKEN CONTENTS ===")
    print(json.dumps(unverified, indent=2))
    print("\n=== KEY FIELDS ===")
    print(f"Audience (aud): {unverified.get('aud')}")
    print(f"Issuer (iss): {unverified.get('iss')}")
    print(f"Subject (sub): {unverified.get('sub')}")
    print(f"Authorized Party (azp): {unverified.get('azp')}")
    print(f"Client ID: {unverified.get('client_id')}")
    print(f"Preferred Username: {unverified.get('preferred_username')}")
except Exception as e:
    print(f"Error decoding token: {e}")
