import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { firstValueFrom, filter, take } from 'rxjs';

export const authGuard = async () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    // Wait until AuthService signals it has finished initialization
    await firstValueFrom(
        authService.isInitialized$.pipe(filter((initialized) => initialized), take(1))
    );

    if (authService.isAuthenticated()) {
        return true;
    }

    router.navigate(['/login']);
    return false;
};

export const roleGuard = (requiredRole: string) => {
    return async () => {
        const authService = inject(AuthService);
        const router = inject(Router);

        // Ensure AuthService is initialized before role checks
        await firstValueFrom(
            authService.isInitialized$.pipe(filter((i) => i), take(1))
        );

        if (!authService.isAuthenticated()) {
            router.navigate(['/login']);
            return false;
        }

        if (authService.hasRole(requiredRole)) {
            return true;
        }

        router.navigate(['/welcome']);
        return false;
    };
};
