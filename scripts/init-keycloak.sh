#!/bin/bash
# Keycloak Initialization Script
# Automatically imports quantum realm on first startup

echo "Waiting for Keycloak to start..."
sleep 30

# Check if realm already exists
REALM_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" \
  http://keycloak:8080/realms/quantum)

if [ "$REALM_EXISTS" == "200" ]; then
  echo "Realm 'quantum' already exists. Skipping import."
  exit 0
fi

echo "Importing quantum realm..."

# Get admin token
ADMIN_TOKEN=$(curl -s -X POST http://keycloak:8080/realms/master/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
  echo "Failed to get admin token"
  exit 1
fi

# Import realm
curl -X POST http://keycloak:8080/admin/realms \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d @/config/quantum-realm.json

if [ $? -eq 0 ]; then
  echo "✅ Quantum realm imported successfully!"
  echo "✅ Test users created: admin, developer, analyst, viewer"
  echo "✅ Groups configured: quantum-admins, quantum-developers, quantum-analysts, quantum-viewers"
  echo ""
  echo "🔐 You can now login at: http://localhost:8080"
else
  echo "❌ Failed to import realm"
  exit 1
fi
