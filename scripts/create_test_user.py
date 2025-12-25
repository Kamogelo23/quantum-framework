"""
Create a test user in Keycloak via REST API
"""
import requests
import json

# Keycloak configuration
KEYCLOAK_URL = "http://localhost:8080"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
REALM = "quantum"

# Step 1: Get admin access token
print("Getting admin access token...")
token_url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
token_data = {
    "client_id": "admin-cli",
    "username": ADMIN_USERNAME,
    "password": ADMIN_PASSWORD,
    "grant_type": "password"
}

response = requests.post(token_url, data=token_data)
if response.status_code != 200:
    print(f"Failed to get token: {response.status_code}")
    print(response.text)
    exit(1)

admin_token = response.json()["access_token"]
print(f"✅ Got admin token")

# Step 2: Create user in quantum realm
print(f"\nCreating user in '{REALM}' realm...")
create_user_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users"
headers = {
    " Authorization": f"Bearer {admin_token}",
    "Content-Type": "application/json"
}

user_data = {
    "username": "testuser",
    "email": "test@quantum.local",
    "firstName": "Test",
    "lastName": "User",
    "enabled": True,
    "emailVerified": True
}

response = requests.post(create_user_url, headers=headers, json=user_data)
if response.status_code == 201:
    print(f"✅ User created successfully!")
    # Get user ID from Location header
    user_location = response.headers.get("Location")
    user_id = user_location.split("/")[-1]
    print(f"User ID: {user_id}")
elif response.status_code == 409:
    print(f"⚠️  User already exists. Fetching user ID...")
    # Search for existing user
    search_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users?username=testuser"
    response = requests.get(search_url, headers=headers)
    users = response.json ()
    if users:
        user_id = users[0]["id"]
        print(f"Found existing user ID: {user_id}")
    else:
        print("Could not find user")
        exit(1)
else:
    print(f"Failed to create user: {response.status_code}")
    print(response.text)
    exit(1)

# Step 3: Set password
print(f"\nSetting password for user...")
password_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users/{user_id}/reset-password"
password_data = {
    "type": "password",
    "value": "Test123!",
    "temporary": False
}

response = requests.put(password_url, headers=headers, json=password_data)
if response.status_code == 204:
    print(f"✅ Password set successfully!")
else:
    print(f"Failed to set password: {response.status_code}")
    print(response.text)
    exit(1)

print("\n" + "="*60)
print("✅ SUCCESS! Test user created:")
print(f"  Username: testuser")
print(f"  Password: Test123!")
print(f"  Email: test@quantum.local")
print("="*60)
print("\nYou can now log in at: http://localhost:4200/login")
