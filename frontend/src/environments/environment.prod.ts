export const environment = {
    production: true,
    keycloak: {
        issuer: 'https://your-keycloak-domain.com/realms/quantum',
        redirectUri: 'https://your-app-domain.com',
        postLogoutRedirectUri: 'https://your-app-domain.com',
        clientId: 'quantum-frontend',
        responseType: 'code',
        scope: 'openid profile email',
        showDebugInformation: false,
        requireHttps: true
    },
    apiUrl: 'https://your-api-domain.com/api/v1'
};
