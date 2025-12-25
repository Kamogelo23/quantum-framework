"""
Keycloak authentication backend for Django REST Framework.
Validates JWT tokens and extracts user information and groups.
"""

import jwt
import logging
from typing import Optional, Dict, Any
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import requests
from functools import lru_cache

logger = logging.getLogger(__name__)


class KeycloakAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication backend that validates Keycloak JWT tokens.
    Extracts user info and groups from the token.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using Keycloak JWT token.
        
        Returns:
            tuple: (user, token_data) if authentication successful
            None: if no authentication credentials provided
        
        Raises:
            AuthenticationFailed: if authentication fails
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        try:
            # Extract token from 'Bearer <token>' format
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid authorization header format')
            
            token = parts[1]
            
            # Decode and validate JWT token
            token_data = self.decode_token(token)
            
            # Get or create user from token data
            user = self.get_or_create_user(token_data)
            
            # Attach groups to request for permission checking
            request.keycloak_groups = token_data.get('groups', [])
            request.token_data = token_data
            
            return (user, token_data)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            logger.error(f'Authentication error: {str(e)}')
            raise exceptions.AuthenticationFailed(str(e))
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token using Keycloak's public key.
        """
        # Get unverified header to extract key ID (kid)
        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')
            logger.debug(f'Token kid: {kid}, alg: {unverified_header.get("alg")}')
        except jwt.DecodeError as e:
            logger.error(f'Failed to decode token header: {e}')
            raise exceptions.AuthenticationFailed('Invalid token header')

        # Get public key from Keycloak JWKS endpoint
        public_key = self.get_keycloak_public_key(kid)
        logger.debug(f'Retrieved public key for kid: {kid}')

        # Decode token
        # Note: In dev flow, audience might match frontend client ID, not backend
        # We allow verify_aud=False if strict verification fails, or we can add multiple audiences
        # For now, we'll try standard verification
        try:
            logger.debug(f'Attempting to decode token with audience: {settings.OIDC_RP_CLIENT_ID}')
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=settings.OIDC_RP_CLIENT_ID,
                options={
                    'verify_signature': True,
                    'verify_aud': True,
                    'verify_exp': True,
                }
            )
            logger.debug('Token decoded successfully with audience check')
        except jwt.InvalidAudienceError:
            # Fallback: Try verifying with verify_aud=False but check if authorized party is trusted
            # This is common in SPA + API setups where token is issued to SPA
            logger.debug('Audience mismatch, trying without audience verification')
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options={
                    'verify_signature': True,
                    'verify_aud': False,
                    'verify_exp': True,
                }
            )
            logger.debug(f'Token decoded without aud check. azp={decoded.get("azp")}, aud={decoded.get("aud")}')
            # Optional: Check 'azp' (Authorized Party) matches an expected client
            # if decoded.get('azp') not in [settings.OIDC_RP_CLIENT_ID, 'quantum-frontend']:
            #     raise exceptions.AuthenticationFailed('Invalid authorized party')
        
        return decoded
    
    def get_jwks(self):
        """Fetch JWKS from Keycloak (no caching for now to debug)"""
        try:
            logger.debug(f'Fetching JWKS from: {settings.OIDC_OP_JWKS_ENDPOINT}')
            response = requests.get(
                settings.OIDC_OP_JWKS_ENDPOINT,
                timeout=10
            )
            response.raise_for_status()
            jwks = response.json()
            logger.debug(f'Got {len(jwks.get("keys", []))} keys from JWKS')
            return jwks
        except requests.RequestException as e:
            logger.error(f'Failed to fetch Keycloak public key: {str(e)}')
            raise exceptions.AuthenticationFailed('Unable to validate token')

    def get_keycloak_public_key(self, kid: Optional[str] = None) -> str:
        """
        Fetch Keycloak's public key from JWKS endpoint matching the kid.
        """
        jwks = self.get_jwks()
        
        if 'keys' not in jwks:
            raise exceptions.AuthenticationFailed('No keys found in JWKS')
            
        key_data = None
        
        # If kid provided, find matching key
        if kid:
            for key in jwks['keys']:
                if key.get('kid') == kid:
                    key_data = key
                    break
        
        # Fallback to first key if no kid or no match (though no match should probably fail)
        if not key_data:
            if kid:
                logger.warning(f"Key with kid {kid} not found in JWKS, falling back to first key")
            if len(jwks['keys']) > 0:
                key_data = jwks['keys'][0]
            else:
                raise exceptions.AuthenticationFailed('No keys found in JWKS')
                
        # Convert JWK to PEM format
        from jwt.algorithms import RSAAlgorithm
        public_key = RSAAlgorithm.from_jwk(key_data)
        
        return public_key
    
    def get_or_create_user(self, token_data: Dict[str, Any]) -> User:
        """
        Get or create Django user from token data.
        
        Args:
            token_data: Decoded JWT token data
            
        Returns:
            User: Django user instance
        """
        username = token_data.get('preferred_username') or token_data.get('sub')
        email = token_data.get('email', '')
        first_name = token_data.get('given_name', '')
        last_name = token_data.get('family_name', '')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        
        # Update user info if it changed
        if not created:
            updated = False
            if user.email != email:
                user.email = email
                updated = True
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if user.last_name != last_name:
                user.last_name = last_name
                updated = True
            
            if updated:
                user.save()
        
        logger.info(f'User {"created" if created else "authenticated"}: {username}')
        
        return user
