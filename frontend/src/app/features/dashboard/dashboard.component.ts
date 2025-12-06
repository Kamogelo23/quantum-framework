import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <h1>Quantum Dashboard</h1>
      <div class="metrics-grid">
        <div class="metric-card">
          <h3>System Health</h3>
          <p class="metric-value">{{ metrics.total }}%</p>
        </div>
        <div class="metric-card">
          <h3>Active Systems</h3>
          <p class="metric-value">{{ metrics.active }}</p>
        </div>
        <div class="metric-card">
          <h3>Error Count</h3>
          <p class="metric-value">{{ metrics.errors }}</p>
        </div>
        <div class="metric-card">
          <h3>Uptime</h3>
          <p class="metric-value">{{ metrics.uptime }}%</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard {
      padding: 2rem;
      color: white;
    }
    
    h1 {
      font-size: 2.5rem;
      margin-bottom: 2rem;
    }
    
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
    }
    
    .metric-card {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 12px;
      padding: 1.5rem;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    h3 {
      font-size: 1rem;
      margin: 0 0 1rem 0;
      opacity: 0.8;
    }
    
    .metric-value {
      font-size: 2.5rem;
      font-weight: bold;
      margin: 0;
    }
  `]
})
export class DashboardComponent {
  metrics = {
    total: 98.5,
    active: 892,
    errors: 12,
    uptime: 99.9
  };

  constructor() { }

  // WebSocket connection will be added later with Django Channels
}
