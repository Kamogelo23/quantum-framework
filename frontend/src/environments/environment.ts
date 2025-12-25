export const environment = {
    production: false,
    keycloak: {
        issuer: 'http://localhost:8080/realms/quantum',
        redirectUri: 'http://localhost:4200',
        postLogoutRedirectUri: 'http://localhost:4200',
        clientId: 'quantum-frontend',
        responseType: 'code',
        scope: 'openid profile email',
        showDebugInformation: true,
        requireHttps: false
    },
    apiUrl: 'http://localhost:8000/api/v1'
};
