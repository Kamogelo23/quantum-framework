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
        <div class="logo-section">
          <div class="logo">Q</div>
          <h1>Quantum</h1>
          <p class="tagline">AI-Powered Monitoring Platform</p>
        </div>
        
        <div class="login-content">
          <h2>Welcome Back</h2>
          <p class="subtitle">Sign in to access your dashboard</p>
          
          <button class="login-button" (click)="login()">
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
            Sign in with Keycloak
          </button>
          
          <div class="features">
            <div class="feature">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <span>Secure Authentication</span>
            </div>
            <div class="feature">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>Real-time Monitoring</span>
            </div>
            <div class="feature">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span>AI-Powered Insights</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
    styles: [`
    .login-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem;
    }

    .login-card {
      background: white;
      border-radius: 24px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      max-width: 450px;
      width: 100%;
      overflow: hidden;
    }

    .logo-section {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 3rem 2rem;
      text-align: center;
      color: white;
    }

    .logo {
      width: 80px;
      height: 80px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2.5rem;
      font-weight: bold;
      margin: 0 auto 1rem;
      backdrop-filter: blur(10px);
    }

    h1 {
      margin: 0;
      font-size: 2rem;
      font-weight: 700;
    }

    .tagline {
      margin: 0.5rem 0 0;
      opacity: 0.9;
      font-size: 0.95rem;
    }

    .login-content {
      padding: 2.5rem 2rem;
    }

    h2 {
      margin: 0 0 0.5rem;
      color: #1a202c;
      font-size: 1.75rem;
    }

    .subtitle {
      margin: 0 0 2rem;
      color: #718096;
      font-size: 0.95rem;
    }

    .login-button {
      width: 100%;
      padding: 1rem 1.5rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
    }

    .login-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }

    .login-button .icon {
      width: 24px;
      height: 24px;
    }

    .features {
      margin-top: 2.5rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .feature {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: #4a5568;
      font-size: 0.9rem;
    }

    .feature svg {
      width: 20px;
      height: 20px;
      color: #667eea;
    }
  `]
})
export class LoginComponent {
    constructor(private authService: AuthService) { }

    login() {
        this.authService.login();
    }
}
