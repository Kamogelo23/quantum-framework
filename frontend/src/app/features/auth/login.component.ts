import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="login-container">
      <div class="login-card">
        <!-- Left Side: Brand -->
        <div class="brand-section">
          <div class="brand-content">
            <div class="logo-wrapper">
              <div class="logo">Q</div>
            </div>
            <h1>Quantum</h1>
            <p class="tagline">The Intelligence Behind Your Infrastructure</p>
            
            <div class="features">
              <div class="feature">
                <div class="feature-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <span>Enterprise Security</span>
              </div>
              <div class="feature">
                <div class="feature-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <span>Real-time Analytics</span>
              </div>
              <div class="feature">
                <div class="feature-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <span>AI-Powered Insights</span>
              </div>
            </div>
          </div>
          
          <div class="brand-footer">
            <p>&copy; 2025 Quantum Systems</p>
          </div>
        </div>
        
        <!-- Right Side: Login -->
        <div class="form-section">
          <div class="form-wrapper">
            <div class="form-header">
              <h2>Welcome Back</h2>
              <p>Please sign in to access your dashboard</p>
            </div>
            
            <button class="login-button" (click)="login()">
              <div class="button-content">
                <svg class="keycloak-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
                </svg>
                <span>Sign in with Keycloak</span>
              </div>
            </button>
            
            <div class="help-link">
              <a href="#">Having trouble signing in?</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .login-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #f3f4f6;
      padding: 2rem;
    }

    .login-card {
      display: flex;
      width: 100%;
      max-width: 960px;
      min-height: 600px;
      background: white;
      border-radius: 20px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      overflow: hidden;
      border: 1px solid rgba(0,0,0,0.05);
    }

    /* Left Side: Brand */
    .brand-section {
      flex: 1;
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      padding: 3rem;
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }

    .brand-section::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMSIgY3k9IjEiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wNSkiLz48L3N2Zz4=');
      opacity: 0.3;
    }

    .brand-content {
      position: relative;
      z-index: 10;
    }

    .logo-wrapper {
      margin-bottom: 2rem;
    }

    .logo {
      width: 64px;
      height: 64px;
      background: white;
      color: #4f46e5;
      font-size: 2rem;
      font-weight: 800;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    h1 {
      font-size: 2.5rem;
      font-weight: 700;
      margin: 0 0 0.5rem;
      letter-spacing: -0.025em;
    }

    .tagline {
      font-size: 1.125rem;
      opacity: 0.9;
      margin-bottom: 3rem;
      font-weight: 400;
    }

    .features {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .feature {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .feature-icon {
      width: 40px;
      height: 40px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(4px);
    }

    .feature-icon svg {
      width: 20px;
      height: 20px;
      color: white;
    }

    .feature span {
      font-weight: 500;
      font-size: 1rem;
    }

    .brand-footer {
      font-size: 0.875rem;
      opacity: 0.6;
      position: relative;
      z-index: 10;
    }

    /* Right Side: Form */
    .form-section {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3rem;
      background: white;
    }

    .form-wrapper {
      width: 100%;
      max-width: 360px;
    }

    .form-header {
      margin-bottom: 2.5rem;
      text-align: center;
    }

    .form-header h2 {
      font-size: 1.875rem;
      color: #111827;
      margin: 0 0 0.5rem;
      font-weight: 700;
    }

    .form-header p {
      color: #6b7280;
      font-size: 0.95rem;
      margin: 0;
    }

    .login-button {
      width: 100%;
      background: #111827; /* Solid Black/Grey */
      color: white;
      border: 1px solid transparent;
      padding: 0.875rem 1.5rem;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }

    .login-button:hover {
      background: #1f2937;
      transform: translateY(-1px);
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .button-content {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
    }

    .keycloak-icon {
      width: 20px;
      height: 20px;
    }

    .help-link {
      margin-top: 1.5rem;
      text-align: center;
    }

    .help-link a {
      color: #6b7280;
      text-decoration: none;
      font-size: 0.875rem;
      transition: color 0.2s;
    }

    .help-link a:hover {
      color: #4f46e5;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .login-card {
        flex-direction: column;
        min-height: auto;
      }

      .brand-section {
        padding: 2rem;
      }

      .form-section {
        padding: 2rem;
      }
    }
  `]
})
export class LoginComponent {
  constructor(private authService: AuthService) {
    console.log('[LoginComponent] Component initialized');
    console.log('[LoginComponent] AuthService injected:', this.authService);
  }

  login() {
    console.log('[LoginComponent] Login button clicked!');
    console.log('[LoginComponent] Calling authService.login()...');
    try {
      this.authService.login();
      console.log('[LoginComponent] authService.login() called successfully');
    } catch (error) {
      console.error('[LoginComponent] Error calling login():', error);
    }
  }
}
