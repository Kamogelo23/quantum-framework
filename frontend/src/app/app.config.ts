import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { OAuthModule } from 'angular-oauth2-oidc';
import { authInterceptor } from './core/interceptors/auth.interceptor';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
    providers: [
        provideRouter(routes),
        provideHttpClient(
            withInterceptors([authInterceptor])
        ),
        importProvidersFrom(OAuthModule.forRoot())
    ]
};
