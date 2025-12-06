import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService, UserProfile } from '../../core/services/auth.service';

@Component({
    selector: 'app-welcome',
    standalone: true,
    imports: [CommonModule, RouterLink],
    template: `
    <div class="welcome-container">
      <div class="header">
        <div>
          <h1>Welcome back, {{ userProfile?.name || 'User' }}! 👋</h1>
          <p class="subtitle">Here's what's happening with your system today</p>
        </div>
        <div class="user-badge">
          <span class="role-badge" [class.admin]="isAdmin" [class.developer]="isDeveloper" [class.analyst]="isAnalyst">
            {{ getUserRole() }}
          </span>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <h3>API Status</h3>
            <p class="stat-value">Healthy</p>
            <p class="stat-label">All systems operational</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
          <div class="stat-content">
            <h3>Data Points</h3>
            <p class="stat-value">24.5K</p>
            <p class="stat-label">Last 24 hours</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div class="stat-content">
            <h3>ML Models</h3>
            <p class="stat-value">5</p>
            <p class="stat-label">Active models</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <h3>Uptime</h3>
            <p class="stat-value">99.9%</p>
            <p class="stat-label">Last 30 days</p>
          </div>
        </div>
      </div>

      <div class="apps-section">
        <h2>Your Applications</h2>
        <div class="apps-grid">
          <a routerLink="/monitoring" class="app-card" *ngIf="isViewer">
            <div class="app-icon"  style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3>Monitoring</h3>
            <p>Real-time data ingestion and queries</p>
            <span class="app-badge">Viewer+</span>
          </a>

          <a routerLink="/ml" class="app-card" *ngIf="isAnalyst">
            <div class="app-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3>ML Insights</h3>
            <p>Predictions and anomaly detection</p>
            <span class="app-badge">Analyst+</span>
          </a>

          <a routerLink="/admin" class="app-card" *ngIf="isAdmin">
            <div class="app-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3>Administration</h3>
            <p>System management and configuration</p>
            <span class="app-badge admin">Admin Only</span>
          </a>
        </div>
      </div>
    </div>
  `,
    styles: [`
    .welcome-container {
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 2rem;
    }

    h1 {
      font-size: 2.5rem;
      margin: 0 0 0.5rem;
      color: #1a202c;
    }

    .subtitle {
      color: #718096;
      font-size: 1.1rem;
      margin: 0;
    }

    .user-badge {
      display: flex;
      gap: 0.5rem;
    }

    .role-badge {
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.875rem;
      font-weight: 600;
      background: #e2e8f0;
      color: #4a5568;
    }

    .role-badge.admin {
      background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
      color: white;
    }

    .role-badge.developer {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .role-badge.analyst {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      color: white;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }

    .stat-card {
      background: white;
      border-radius: 16px;
      padding: 1.5rem;
      display: flex;
      gap: 1rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .stat-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .stat-icon svg {
      width: 30px;
      height: 30px;
      color: white;
    }

    .stat-content h3 {
      margin: 0 0 0.5rem;
      color: #718096;
      font-size: 0.9rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      margin: 0;
      color: #1a202c;
    }

    .stat-label {
      margin: 0.25rem 0 0;
      color: #a0aec0;
      font-size: 0.875rem;
    }

    .apps-section h2 {
      font-size: 1.75rem;
      margin: 0 0 1.5rem;
      color: #1a202c;
    }

    .apps-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
    }

    .app-card {
      background: white;
      border-radius: 16px;
      padding: 2rem;
      text-decoration: none;
      color: inherit;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      transition: transform 0.2s, box-shadow 0.2s;
      position: relative;
      overflow: hidden;
    }

    .app-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }

    .app-card::before{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    .app-icon {
      width: 70px;
      height: 70px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1.5rem;
    }

    .app-icon svg {
      width: 36px;
      height: 36px;
      color: white;
    }

    .app-card h3 {
      margin: 0 0 0.5rem;
      font-size: 1.5rem;
      color: #1a202c;
    }

    .app-card p {
      margin: 0 0 1rem;
      color: #718096;
      line-height: 1.6;
    }

    .app-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      background: #edf2f7;
      color: #4a5568;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .app-badge.admin {
      background: rgba(250, 112, 154, 0.1);
      color: #fa709a;
    }
  `]
})
export class WelcomeComponent implements OnInit {
    userProfile: UserProfile | null = null;
    isAdmin = false;
    isDeveloper = false;
    isAnalyst = false;
    isViewer = false;

    constructor(private authService: AuthService) { }

    ngOnInit() {
        this.authService.userProfile$.subscribe(profile => {
            this.userProfile = profile;
        });

        this.isAdmin = this.authService.isAdmin();
        this.isDeveloper = this.authService.isDeveloper();
        this.isAnalyst = this.authService.isAnalyst();
        this.isViewer = this.authService.isViewer();
    }

    getUserRole(): string {
        if (this.isAdmin) return 'Admin';
        if (this.isDeveloper) return 'Developer';
        if (this.isAnalyst) return 'Analyst';
        if (this.isViewer) return 'Viewer';
        return 'User';
    }
}
