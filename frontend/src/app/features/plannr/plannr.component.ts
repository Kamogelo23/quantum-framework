import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Component({
    selector: 'app-plannr',
    templateUrl: './plannr.component.html',
    styleUrls: ['./plannr.component.css'],
    standalone: true,
    imports: [CommonModule, FormsModule]
})
export class PlannrComponent {
    jobText: string = '';
    jobFile: File | null = null;
    resumeFile: File | null = null;
    keywords: string[] = [];
    tailoredId: number | null = null;
    downloadUrl: string = '';
    loading = false;
    loadingStep: string = '';

    constructor(private http: HttpClient) { }

    onJobFileChange(event: any) {
        const file = event.target.files[0];
        if (file) this.jobFile = file;
    }

    onResumeFileChange(event: any) {
        const file = event.target.files[0];
        if (file) this.resumeFile = file;
    }

    async submit() {
        this.loading = true;
        this.loadingStep = '🚀 Preparing files for upload...';

        try {
            // 1. Upload job description
            this.loadingStep = '📤 Uploading job description...';
            const jobForm = new FormData();
            if (this.jobFile) {
                jobForm.append('file', this.jobFile);
            } else {
                jobForm.append('content', this.jobText);
            }
            const jobResp: any = await this.http.post(`${environment.apiUrl}/plannr/job-description/`, jobForm).toPromise();
            const jobId = jobResp.id;

            // 2. Upload resume
            this.loadingStep = '📄 Uploading your resume...';
            const resumeForm = new FormData();
            if (this.resumeFile) resumeForm.append('file', this.resumeFile);
            const resumeResp: any = await this.http.post(`${environment.apiUrl}/plannr/resume/`, resumeForm).toPromise();
            const resumeId = resumeResp.id;

            // 3. Extract keywords
            this.loadingStep = '🤖 Gemini AI is analyzing job requirements...';
            const kwResp: any = await this.http.post(`${environment.apiUrl}/plannr/analyze/`, { job_id: jobId }).toPromise();
            this.keywords = kwResp.keywords;

            // 4. Tailor resume
            this.loadingStep = '✨ Tailoring your resume with identified keywords...';
            const tailorResp: any = await this.http.post(`${environment.apiUrl}/plannr/tailor/`, {
                job_id: jobId,
                resume_id: resumeId,
                keywords: this.keywords
            }).toPromise();
            this.tailoredId = tailorResp.id;

            // 5. Get download link
            this.loadingStep = '🔨 Generating final PDF...';
            const dlResp: any = await this.http.get(`${environment.apiUrl}/plannr/download/${this.tailoredId}/`).toPromise();
            this.downloadUrl = dlResp.download_url;

            this.loadingStep = '✅ Done!';
        } catch (err) {
            console.error('Plannr error', err);
            this.loadingStep = '❌ Error occurred. Please try again.';
        } finally {
            this.loading = false;
        }
    }
}
