import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-admin',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="admin-container">
      <div class="admin-header">
        <h1>🛠️ Administration</h1>
        <p class="subtitle">System management and configuration</p>
      </div>

      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-header">
            <h2>👥 User Management</h2>
            <span class="badge">{{ users.length }} Users</span>
          </div>
          <div class="card-content">
            <div class="user-list">
              <div class="user-item" *ngFor="let user of users">
                <div class="user-avatar">{{ user.name.charAt(0) }}</div>
                <div class="user-info">
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-email">{{ user.email }}</div>
                </div>
                <span class="role-badge" [ngClass]="user.role.toLowerCase()">
                  {{ user.role }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="admin-card">
          <div class="card-header">
            <h2>📊 System Metrics</h2>
            <span class="badge success">Healthy</span>
          </div>
          <div class="card-content">
            <div class="metric-grid">
              <div class="metric">
                <div class="metric-label">CPU Usage</div>
                <div class="metric-value">45%</div>
                <div class="metric-bar">
                  <div class="metric-bar-fill" style="width: 45%;"></div>
                </div>
              </div>
              <div class="metric">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value">62%</div>
                <div class="metric-bar">
                  <div class="metric-bar-fill" style="width: 62%; background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);"></div>
                </div>
              </div>
              <div class="metric">
                <div class="metric-label">Disk Usage</div>
                <div class="metric-value">38%</div>
                <div class="metric-bar">
                  <div class="metric-bar-fill" style="width: 38%; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);"></div>
                </div>
              </div>
              <div class="metric">
                <div class="metric-label">Network I/O</div>
                <div class="metric-value">28%</div>
                <div class="metric-bar">
                  <div class="metric-bar-fill" style="width: 28%; background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="admin-card full-width">
          <div class="card-header">
            <h2>⚙️ System Configuration</h2>
          </div>
          <div class="card-content">
            <div class="config-grid">
              <div class="config-item">
                <div class="config-label">Keycloak Realm</div>
                <div class="config-value">quantum</div>
              </div>
              <div class="config-item">
                <div class="config-label">Backend API</div>
                <div class="config-value">http://localhost:8000</div>
              </div>
              <div class="config-item">
                <div class="config-label">WebSocket</div>
                <div class="config-value">ws://localhost:8000</div>
              </div>
              <div class="config-item">
                <div class="config-label">ML Service</div>
                <div class="config-value">http://localhost:8001</div>
              </div>
              <div class="config-item">
                <div class="config-label">Database</div>
                <div class="config-value">PostgreSQL 16</div>
              </div>
              <div class="config-item">
                <div class="config-label">Cache</div>
                <div class="config-value">Redis 7</div>
              </div>
              <div class="config-item">
                <div class="config-label">Message Queue</div>
                <div class="config-value">RabbitMQ 3</div>
              </div>
              <div class="config-item">
                <div class="config-label">CORS Enabled</div>
                <div class="config-value">✓ Yes</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
    styles: [`
    .admin-container {
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    .admin-header {
      margin-bottom: 2rem;
    }

    .admin-header h1 {
      font-size: 2.5rem;
      margin: 0 0 0.5rem;
      color: #1a202c;
    }

    .subtitle {
      color: #718096;
      font-size: 1.1rem;
      margin: 0;
    }

    .admin-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
      gap: 1.5rem;
    }

    .admin-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    }

    .admin-card.full-width {
      grid-column: 1 / -1;
    }

    .card-header {
      padding: 1.5rem;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .card-header h2 {
      margin: 0;
      font-size: 1.25rem;
      color: #1a202c;
    }

    .badge {
      padding: 0.375rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
      background: #edf2f7;
      color: #4a5568;
    }

    .badge.success {
      background: rgba(72, 187, 120, 0.1);
      color: #48bb78;
    }

    .card-content {
      padding: 1.5rem;
    }

    .user-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .user-item {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
      background: #f7fafc;
      border-radius: 12px;
      transition: background 0.2s;
    }

    .user-item:hover {
      background: #edf2f7;
    }

    .user-avatar {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 1.25rem;
    }

    .user-info {
      flex: 1;
    }

    .user-name {
      font-weight: 600;
      color: #1a202c;
      margin-bottom: 0.25rem;
    }

    .user-email {
      font-size: 0.875rem;
      color: #718096;
    }

    .role-badge {
      padding: 0.375rem 0.75rem;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .role-badge.admin {
      background: rgba(250, 112, 154, 0.1);
      color: #fa709a;
    }

    .role-badge.developer {
      background: rgba(102, 126, 234, 0.1);
      color: #667eea;
    }

    .role-badge.analyst {
      background: rgba(79, 172, 254, 0.1);
      color: #4facfe;
    }

    .role-badge.viewer {
      background: rgba(160, 174, 192, 0.1);
      color: #a0aec0;
    }

    .metric-grid {
      display: grid;
      gap: 1.5rem;
    }

    .metric {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .metric-label {
      font-size: 0.875rem;
      color: #718096;
      font-weight: 600;
    }

    .metric-value {
      font-size: 1.5rem;
      font-weight: 700;
      color: #1a202c;
    }

    .metric-bar {
      width: 100%;
      height: 8px;
      background: #e2e8f0;
      border-radius: 4px;
      overflow: hidden;
    }

    .metric-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
      border-radius: 4px;
      transition: width 0.3s ease;
    }

    .config-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1.5rem;
    }

    .config-item {
      padding: 1rem;
      background: #f7fafc;
      border-radius: 12px;
      border-left: 4px solid #667eea;
    }

    .config-label {
      font-size: 0.875rem;
      color: #718096;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }

    .config-value {
      font-size: 1rem;
      color: #1a202c;
      font-weight: 500;
      font-family: 'Monaco', 'Menlo', monospace;
    }
  `]
})
export class AdminComponent {
    users = [
        { name: 'Admin User', email: 'admin@quantum.com', role: 'Admin' },
        { name: 'John Developer', email: 'john@quantum.com', role: 'Developer' },
        { name: 'Jane Analyst', email: 'jane@quantum.com', role: 'Analyst' },
        { name: 'Bob Viewer', email: 'bob@quantum.com', role: 'Viewer' }
    ];
}
