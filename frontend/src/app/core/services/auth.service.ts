import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from '../auth.config';
import { BehaviorSubject, Observable } from 'rxjs';

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
    private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
    public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

    private userProfileSubject = new BehaviorSubject<UserProfile | null>(null);
    public userProfile$ = this.userProfileSubject.asObservable();

    constructor(
        private oauthService: OAuthService,
        private router: Router
    ) {
        this.configure();
    }

    private configure() {
        this.oauthService.configure(authConfig);
        this.oauthService.setupAutomaticSilentRefresh();
        this.oauthService.loadDiscoveryDocumentAndTryLogin().then(() => {
            if (this.oauthService.hasValidAccessToken()) {
                this.isAuthenticatedSubject.next(true);
                this.loadUserProfile();
            }
        });
    }

    public login() {
        this.oauthService.initCodeFlow();
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
        return this.oauthService.getAccessToken();
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
