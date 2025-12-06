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
        
        Args:
            token: JWT token string
            
        Returns:
            dict: Decoded token data
        """
        # Get public key from Keycloak JWKS endpoint
        public_key = self.get_keycloak_public_key()
        
        # Decode token
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
        
        return decoded
    
    @lru_cache(maxsize=1)
    def get_keycloak_public_key(self) -> str:
        """
        Fetch Keycloak's public key from JWKS endpoint.
        Cached to avoid repeated requests.
        
        Returns:
            str: PEM-formatted public key
        """
        try:
            response = requests.get(
                settings.OIDC_OP_JWKS_ENDPOINT,
                timeout=10
            )
            response.raise_for_status()
            jwks = response.json()
            
            # Get the first key (you might want to select by kid in production)
            if 'keys' in jwks and len(jwks['keys']) > 0:
                key_data = jwks['keys'][0]
                
                # Convert JWK to PEM format
                from jwt.algorithms import RSAAlgorithm
                public_key = RSAAlgorithm.from_jwk(key_data)
                
                return public_key
            else:
                raise exceptions.AuthenticationFailed('No keys found in JWKS')
                
        except requests.RequestException as e:
            logger.error(f'Failed to fetch Keycloak public key: {str(e)}')
            raise exceptions.AuthenticationFailed('Unable to validate token')
    
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
