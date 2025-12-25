import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
    const authService = inject(AuthService);

    // Skip authentication for certain URLs
    const skipAuthUrls = [
        '/assets/',
        '/silent-refresh',
        '.well-known',      // Skip discovery document calls
        '/realms/',         // Skip all Keycloak realm calls
        'protocol/openid-connect'
    ];

    const shouldSkipAuth = skipAuthUrls.some(url => req.url.includes(url));

    if (shouldSkipAuth) {
        console.log('[AuthInterceptor] Skipping auth for URL:', req.url);
        return next(req);
    }

    // Get the access token from the auth service
    const token = authService.getAccessToken();

    if (token) {
        console.log('[AuthInterceptor] Adding Bearer token to request:', req.url);
        const cloned = req.clone({
            setHeaders: {
                Authorization: `Bearer ${token}`
            }
        });
        return next(cloned);
    } else {
        console.log('[AuthInterceptor] No token available for request:', req.url);
    }

    return next(req);
};

