from django.db import models

class JobDescription(models.Model):
    """Stores a job description either pasted as text or uploaded as a file."""
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    uploaded_file = models.FileField(upload_to='plannr/job_descriptions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"JobDescription {self.id}" 

class Resume(models.Model):
    """Stores the original resume uploaded by the user."""
    candidate_name = models.CharField(max_length=255, blank=True)
    uploaded_file = models.FileField(upload_to='plannr/resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name or f"Resume {self.id}" 

class TailoredResume(models.Model):
    """Result of the tailoring process – LaTeX source and compiled PDF."""
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='tailored_resumes')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='tailored_resumes')
    keywords = models.JSONField(default=list, blank=True)
    latex_source = models.TextField()
    pdf_file = models.FileField(upload_to='plannr/outputs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TailoredResume {self.id}"
