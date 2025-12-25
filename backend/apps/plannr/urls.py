from django.urls import path
from . import views

urlpatterns = [
    path('job-description/', views.JobDescriptionUploadView.as_view(), name='job_description_upload'),
    path('resume/', views.ResumeUploadView.as_view(), name='resume_upload'),
    path('analyze/', views.AnalyzeView.as_view(), name='analyze'),
    path('tailor/', views.TailorView.as_view(), name='tailor'),
    path('download/<int:pk>/', views.DownloadView.as_view(), name='download'),
]
