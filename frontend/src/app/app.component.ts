import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { AuthService, UserProfile } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="app-layout" *ngIf="isAuthenticated; else loginView">
      <nav class="sidebar">
        <div class="logo-section">
          <div class="logo">Q</div>
          <h2>Quantum</h2>
        </div>

        <div class="nav-links">
          <a routerLink="/welcome" routerLinkActive="active" class="nav-link">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span>Home</span>
          </a>

          <a routerLink="/monitoring" routerLinkActive="active" class="nav-link" *ngIf="isViewer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span>Monitoring</span>
          </a>

          <a routerLink="/ml" routerLinkActive="active" class="nav-link" *ngIf="isAnalyst">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <span>ML Insights</span>
          </a>

          <a routerLink="/admin" routerLinkActive="active" class="nav-link" *ngIf="isAdmin">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>Admin</span>
          </a>
        </div>

        <div class="sidebar-footer">
          <div class="user-profile">
            <div class="user-avatar">{{ getUserInitial() }}</div>
            <div class="user-info">
              <div class="user-name">{{ userProfile?.name || 'User' }}</div>
              <div class="user-role">{{ getUserRole() }}</div>
            </div>
          </div>
          <button class="logout-btn" (click)="logout()">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Logout
          </button>
        </div>
      </nav>

      <main class="main-content">
        <router-outlet></router-outlet>
      </main>
    </div>

    <ng-template #loginView>
      <router-outlet></router-outlet>
    </ng-template>
  `,
  styles: [`
    .app-layout {
      display: flex;
      min-height: 100vh;
      background: #f7fafc;
    }

    .sidebar {
      width: 280px;
      background: white;
      border-right: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      position: fixed;
      height: 100vh;
      left: 0;
      top: 0;
    }

    .logo-section {
      padding: 2rem 1.5rem;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .logo {
      width: 50px;
      height: 50px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      font-size: 1.5rem;
    }

    .logo-section h2 {
      margin: 0;
      font-size: 1.5rem;
      color: #1a202c;
    }

    .nav-links {
      flex: 1;
      padding: 1.5rem 0.75rem;
      overflow-y: auto;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 0.875rem 1rem;
      margin-bottom: 0.5rem;
      border-radius: 12px;
      text-decoration: none;
      color: #718096;
      font-weight: 500;
      transition: all 0.2s;
    }

    .nav-link svg {
      width: 24px;
      height: 24px;
    }

    .nav-link:hover {
      background: #f7fafc;
      color: #667eea;
    }

    .nav-link.active {
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
      color: #667eea;
      font-weight: 600;
    }

    .sidebar-footer {
      padding: 1.5rem;
      border-top: 1px solid #e2e8f0;
    }

    .user-profile {
      display: flex;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1rem;
    }

    .user-avatar {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 1.125rem;
    }

    .user-info {
      flex: 1;
      min-width: 0;
    }

    .user-name {
      font-weight: 600;
      color: #1a202c;
      font-size: 0.95rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .user-role {
      font-size: 0.8rem;
      color: #718096;
    }

    .logout-btn {
      width: 100%;
      padding: 0.75rem 1rem;
      background: #f7fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      color: #718096;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      cursor: pointer;
      transition: all 0.2s;
    }

    .logout-btn svg {
      width: 20px;
      height: 20px;
    }

    .logout-btn:hover {
      background: #edf2f7;
      color: #1a202c;
      border-color: #cbd5e0;
    }

    .main-content {
      margin-left: 280px;
      flex: 1;
      min-height: 100vh;
      background: #f7fafc;
    }
  `]
})
export class AppComponent implements OnInit {
  title = 'Quantum';
  isAuthenticated = false;
  isAdmin = false;
  isDeveloper = false;
  isAnalyst = false;
  isViewer = false;
  userProfile: UserProfile | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    this.authService.isAuthenticated$.subscribe(isAuth => {
      this.isAuthenticated = isAuth;
      if (!isAuth && !this.router.url.includes('/login')) {
        this.router.navigate(['/login']);
      }
    });

    this.authService.userProfile$.subscribe(profile => {
      this.userProfile = profile;
    });

    this.isAdmin = this.authService.isAdmin();
    this.isDeveloper = this.authService.isDeveloper();
    this.isAnalyst = this.authService.isAnalyst();
    this.isViewer = this.authService.isViewer();
  }

  getUserRole(): string {
    if (this.isAdmin) return 'Administrator';
    if (this.isDeveloper) return 'Developer';
    if (this.isAnalyst) return 'Analyst';
    if (this.isViewer) return 'Viewer';
    return 'User';
  }

  getUserInitial(): string {
    return this.userProfile?.name?.charAt(0).toUpperCase() || 'U';
  }

  logout() {
    this.authService.logout();
  }
}
