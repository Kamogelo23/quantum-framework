import { Routes } from '@angular/router';
import { authGuard, roleGuard } from './core/guards/auth.guard';

export const routes: Routes = [
    {
        path: 'login',
        loadComponent: () => import('./features/auth/login.component').then(m => m.LoginComponent)
    },
    {
        path: '',
        canActivate: [authGuard],
        children: [
            {
                path: '',
                redirectTo: 'welcome',
                pathMatch: 'full'
            },
            {
                path: 'welcome',
                loadComponent: () => import('./features/welcome/welcome.component').then(m => m.WelcomeComponent)
            },
            {
                path: 'monitoring',
                loadComponent: () => import('./features/monitoring/monitoring.component').then(m => m.MonitoringComponent),
                canActivate: [roleGuard('viewer')]
            },
            {
                path: 'ml',
                loadComponent: () => import('./features/ml-insights/ml-insights.component').then(m => m.MlInsightsComponent),
                canActivate: [roleGuard('analyst')]
            },
            {
                path: 'admin',
                loadComponent: () => import('./features/admin/admin.component').then(m => m.AdminComponent),
                canActivate: [roleGuard('admin')],
            },
            {
                path: 'plannr',
                loadComponent: () => import('./features/plannr/plannr.component').then(m => m.PlannrComponent),
                canActivate: [authGuard]
            }
        ]
    },
    {
        path: '**',
        redirectTo: ''
    }
];
