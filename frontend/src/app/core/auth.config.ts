import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
    issuer: 'http://localhost:8080/realms/quantum',
    redirectUri: window.location.origin,
    clientId: 'quantum-frontend',
    responseType: 'code',
    scope: 'openid profile email',
    showDebugInformation: true,
    requireHttps: false, // Set to true in production
    useSilentRefresh: true,
    silentRefreshRedirectUri: window.location.origin + '/assets/silent-refresh.html',
};
