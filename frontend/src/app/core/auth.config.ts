import { AuthConfig } from 'angular-oauth2-oidc';
import { environment } from '../../environments/environment';

export const authConfig: AuthConfig = {
    // Identity Provider
    issuer: environment.keycloak.issuer,

    // URL of the SPA to redirect the user to after login
    redirectUri: environment.keycloak.redirectUri,

    // Logout redirect
    postLogoutRedirectUri: environment.keycloak.postLogoutRedirectUri,

    // The SPA's id (client id in Keycloak)
    clientId: environment.keycloak.clientId,

    // Set the responseType to 'code' for authorization code flow
    responseType: environment.keycloak.responseType,

    // Set the requested scopes
    scope: environment.keycloak.scope,

    // Debug output
    showDebugInformation: environment.keycloak.showDebugInformation,

    // For dev environment, disable HTTPS requirement
    requireHttps: environment.keycloak.requireHttps,

    // Silent refresh configuration
    useSilentRefresh: true,
    silentRefreshRedirectUri: `${environment.keycloak.redirectUri}/assets/silent-refresh.html`,

    // Session checks configuration
    sessionChecksEnabled: true,

    // Disable strict discovery document validation for development
    strictDiscoveryDocumentValidation: false,

    // Timeout for HTTP calls to Keycloak (in ms)
    timeoutFactor: 0.75,

    // Automatically refresh tokens before they expire
    sessionCheckIntervall: 3000,

    // Clear hash after login
    clearHashAfterLogin: true,

    // Check token expiration automatically
    oidc: true,

    // Skip issuer check (useful when Keycloak is behind a proxy)
    skipIssuerCheck: false,

    // Disable PKCE for public clients (Keycloak handles this)
    disablePKCE: false,

    // Log out configuration
    logoutUrl: `${environment.keycloak.issuer}/protocol/openid-connect/logout`,
};
