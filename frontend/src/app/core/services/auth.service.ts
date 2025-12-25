import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from '../auth.config';
import { BehaviorSubject } from 'rxjs';
import { firstValueFrom, filter, take } from 'rxjs';

export interface UserProfile {
    sub: string;
    name: string;
    preferred_username: string;
    email: string;
    groups: string[];
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private isInitializedSubject = new BehaviorSubject<boolean>(false);
    public isInitialized$ = this.isInitializedSubject.asObservable();
    private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
    public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

    private userProfileSubject = new BehaviorSubject<UserProfile | null>(null);
    public userProfile$ = this.userProfileSubject.asObservable();

    constructor(
        private oauthService: OAuthService,
        private router: Router
    ) {
        console.log('[AuthService] Constructor called');
        this.configure();
    }

    private configure() {
        console.log('[AuthService] 🔧 Configuring OAuth...');
        console.log('[AuthService] 📋 Config:', authConfig);

        // Configure the OAuth service
        this.oauthService.configure(authConfig);

        // Setup event listeners for debugging
        this.setupOAuthEvents();

        // Setup automatic silent refresh
        this.oauthService.setupAutomaticSilentRefresh();

        // Load discovery document and try to login
        console.log('[AuthService] 🔍 Loading discovery document from:', authConfig.issuer);

        this.oauthService.loadDiscoveryDocumentAndTryLogin()
            .then(() => {
                console.log('[AuthService] ✅ Discovery document loaded successfully');
                this.isInitializedSubject.next(true);

                if (this.oauthService.hasValidAccessToken()) {
                    console.log('[AuthService] ✅ User authenticated successfully');
                    // try {
                    //     const token = this.oauthService.getAccessToken();
                    //     if (token) {
                    //         console.log('[AuthService] 🎫 Access Token:', token.substring(0, 50) + '...');
                    //     }
                    // } catch (e) {
                    //     console.log('[AuthService] ⚠️ Could not retrieve access token for logging');
                    // }
                    this.isAuthenticatedSubject.next(true);
                    this.isAuthenticatedSubject.next(true);
                    try {
                        this.loadUserProfile();
                    } catch (e) {
                        console.warn('[AuthService] Failed to load user profile:', e);
                    }

                    // Navigate to welcome page after successful login
                    if (this.router.url === '/login' || this.router.url === '/') {
                        console.log('[AuthService] 🔄 Redirecting to /welcome');
                        this.router.navigate(['/welcome']);
                    }
                } else {
                    console.log('[AuthService] ⚠️ No valid access token found');
                    this.isAuthenticatedSubject.next(false);
                }
            })
            .catch((err: any) => {
                console.error('[AuthService] ❌ OAuth configuration error:', err);
                console.error('[AuthService] 📍 Error details:', {
                    message: err.message,
                    stack: err.stack,
                    issuer: authConfig.issuer
                });

                // Retry logic for network issues
                console.log('[AuthService] 🔄 Retrying discovery document load in 3 seconds...');
                setTimeout(() => {
                    this.retryLoadDiscovery();
                }, 3000);

                this.isInitializedSubject.next(true);
                this.isAuthenticatedSubject.next(false);
            });
    }

    private setupOAuthEvents() {
        console.log('[AuthService] 📡 Setting up OAuth event listeners...');

        this.oauthService.events.subscribe((event: any) => {
            console.log('[AuthService] 📢 OAuth Event:', event.type, event);

            if (event.type === 'discovery_document_loaded') {
                console.log('[AuthService] 📄 Discovery document loaded event');
            } else if (event.type === 'token_received') {
                console.log('[AuthService] 🎫 Token received event');
            } else if (event.type === 'token_error') {
                console.error('[AuthService] ❌ Token error event:', event);
            } else if (event.type === 'token_expires') {
                console.log('[AuthService] ⏰ Token expiring soon');
            } else if (event.type === 'session_terminated') {
                console.log('[AuthService] 🚪 Session terminated');
            } else if (event.type === 'user_profile_loaded') {
                console.log('[AuthService] 👤 User profile loaded');
            }
        });
    }

    private retryLoadDiscovery() {
        console.log('[AuthService] 🔄 Attempting to reload discovery document...');

        this.oauthService.loadDiscoveryDocument()
            .then(() => {
                console.log('[AuthService] ✅ Discovery document loaded on retry');
                return this.oauthService.tryLogin();
            })
            .then(() => {
                if (this.oauthService.hasValidAccessToken()) {
                    console.log('[AuthService] ✅ User authenticated after retry');
                    this.isAuthenticatedSubject.next(true);
                    this.loadUserProfile();
                }
            })
            .catch((err: any) => {
                console.error('[AuthService] ❌ Retry failed:', err);
                console.error('[AuthService] 💡 Possible issues:');
                console.error('  1. Keycloak is not running at:', authConfig.issuer);
                console.error('  2. Realm "quantum" does not exist');
                console.error('  3. Network connectivity issues');
                console.error('  4. CORS not configured properly on Keycloak');
            });
    }

    public login() {
        console.log('[AuthService] 🚀 login() called');
        console.log('[AuthService] 📍 Current URL:', window.location.href);
        console.log('[AuthService] 🔐 Initiating OAuth code flow...');
        console.log('[AuthService] 🎯 Will redirect to:', authConfig.issuer);

        try {
            // Always try to load discovery document before initiating code flow
            console.log('[AuthService] 🔄 Loading discovery document before login...');
            this.oauthService.loadDiscoveryDocument()
                .then(() => {
                    console.log('[AuthService] ✅ Discovery document loaded, initiating code flow');
                    console.log('[AuthService] 🔄 Redirecting to authorization endpoint...');
                    this.oauthService.initCodeFlow();
                    console.log('[AuthService] ✅ initCodeFlow() executed - browser should redirect now');
                })
                .catch((err: any) => {
                    console.error('[AuthService] ❌ Failed to load discovery document:', err);
                    console.error('[AuthService] 💡 Please check if Keycloak is running at:', authConfig.issuer);
                });
        } catch (error) {
            console.error('[AuthService] ❌ Error in initCodeFlow():', error);
            console.error('[AuthService] 📋 Error details:', {
                message: (error as Error).message,
                stack: (error as Error).stack
            });
        }
    }

    public logout() {
        this.oauthService.logOut();
        this.isAuthenticatedSubject.next(false);
        this.userProfileSubject.next(null);
        this.router.navigate(['/login']);
    }

    public async loadUserProfile(): Promise<void> {
        const claims = this.oauthService.getIdentityClaims() as any;
        if (claims) {
            const profile: UserProfile = {
                sub: claims.sub,
                name: claims.name || claims.preferred_username,
                preferred_username: claims.preferred_username,
                email: claims.email,
                groups: claims.groups || []
            };
            this.userProfileSubject.next(profile);
        }
    }

    public getAccessToken(): string {
        try {
            return this.oauthService.getAccessToken();
        } catch (e) {
            return '';
        }
    }

    public isAuthenticated(): boolean {
        return this.oauthService.hasValidAccessToken();
    }

    // Role checking methods
    public isAdmin(): boolean {
        const profile = this.userProfileSubject.value;
        return profile?.groups?.includes('/quantum-admins') || false;
    }

    public isDeveloper(): boolean {
        const profile = this.userProfileSubject.value;
        return this.isAdmin() || profile?.groups?.includes('/quantum-developers') || false;
    }

    public isAnalyst(): boolean {
        const profile = this.userProfileSubject.value;
        return this.isDeveloper() || profile?.groups?.includes('/quantum-analysts') || false;
    }

    public isViewer(): boolean {
        const profile = this.userProfileSubject.value;
        return this.isAnalyst() || profile?.groups?.includes('/quantum-viewers') || false;
    }

    public hasRole(role: string): boolean {
        switch (role.toLowerCase()) {
            case 'admin': return this.isAdmin();
            case 'developer': return this.isDeveloper();
            case 'analyst': return this.isAnalyst();
            case 'viewer': return this.isViewer();
            default: return false;
        }
    }
}
