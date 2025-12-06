import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-monitoring',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="monitoring">
      <h1>System Monitoring</h1>
      <p>Real-time monitoring dashboard coming soon...</p>
    </div>
  `,
    styles: [`
    .monitoring {
      padding: 2rem;
      color: white;
    }
  `]
})
export class MonitoringComponent { }
