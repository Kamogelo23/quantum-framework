import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-ml-insights',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="ml-insights">
      <h1>ML Insights</h1>
      <p>Machine learning predictions and anomaly detection coming soon...</p>
    </div>
  `,
    styles: [`
    .ml-insights {
      padding: 2rem;
      color: white;
    }
  `]
})
export class MlInsightsComponent { }
