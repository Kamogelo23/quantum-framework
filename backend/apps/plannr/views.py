# Force reload
from rest_framework import status, views, parsers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import JobDescription, Resume, TailoredResume
from .services.keyword_extractor import extract_keywords, parse_resume_data
from .services.text_extractor import extract_text_from_file
from django.core.files import File
from django.conf import settings
import os
from .services.latex_generator import generate_pdf

class JobDescriptionUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = [AllowAny]  # Temporarily disable auth
    
    def post(self, request, *args, **kwargs):
        # Accept text or file upload
        content = request.data.get('content')
        uploaded_file = request.FILES.get('file')
        job = JobDescription.objects.create(content=content or '', uploaded_file=uploaded_file)
        return Response({'id': job.id}, status=status.HTTP_201_CREATED)

class ResumeUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = [AllowAny]  # Temporarily disable auth

    def post(self, request, *args, **kwargs):
        candidate_name = request.data.get('candidate_name', '')
        uploaded_file = request.FILES.get('file')
        resume = Resume.objects.create(candidate_name=candidate_name, uploaded_file=uploaded_file)
        return Response({'id': resume.id}, status=status.HTTP_201_CREATED)

class AnalyzeView(views.APIView):
    permission_classes = [AllowAny]  # Temporarily disable auth
    def post(self, request, *args, **kwargs):
        job_id = request.data.get('job_id')
        try:
            job = JobDescription.objects.get(id=job_id)
        except JobDescription.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
            
        # Extract text from file if content is empty
        text_content = job.content
        if not text_content and job.uploaded_file:
            try:
                text_content = extract_text_from_file(job.uploaded_file.path)
            except Exception as e:
                print(f"Error extracting job text: {e}")
                
        # Use simple extraction (Gemini/Claude/Simple)
        keywords = extract_keywords(text_content or "")
        return Response({'keywords': keywords}, status=status.HTTP_200_OK)

class TailorView(views.APIView):
    permission_classes = [AllowAny]  # Temporarily disable auth
    def post(self, request, *args, **kwargs):
        job_id = request.data.get('job_id')
        resume_id = request.data.get('resume_id')
        keywords = request.data.get('keywords', [])
        try:
            job = JobDescription.objects.get(id=job_id)
            resume = Resume.objects.get(id=resume_id)
        except (JobDescription.DoesNotExist, Resume.DoesNotExist):
            return Response({'error': 'Job or Resume not found'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            # 1. Extract text from resume
            resume_text = ""
            if resume.uploaded_file:
                try:
                    print(f"[DEBUG] Extracting text from: {resume.uploaded_file.path}")
                    resume_text = extract_text_from_file(resume.uploaded_file.path)
                    print(f"[DEBUG] Extracted text length: {len(resume_text)} chars")
                except Exception as e:
                    print(f"[ERROR] Text extraction failed: {e}")
                    import traceback
                    traceback.print_exc()

            # 1b. Extract text from job description
            job_text = job.content
            if not job_text and job.uploaded_file:
                try:
                    job_text = extract_text_from_file(job.uploaded_file.path)
                except Exception as e:
                    print(f"[ERROR] Job text extraction failed: {e}")
            
            # 2. Parse structured data using AI (and tailor if job text exists)
            resume_data = {}
            if resume_text:
                print(f"[DEBUG] Calling AI parser with tailoring...")
                try:
                    resume_data = parse_resume_data(resume_text, job_description=job_text)
                    print(f"[DEBUG] Parsed resume data keys: {list(resume_data.keys())}")
                except Exception as e:
                    print(f"[ERROR] AI parsing failed: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"[WARNING] No resume text to parse!")
                
            # 3. Generate PDF with real data
            pdf_path = generate_pdf(job, resume, keywords, resume_data=resume_data)
            
            tailored = TailoredResume.objects.create(
                job=job,
                resume=resume,
                keywords=keywords,
                latex_source="", # Not using LaTeX anymore
            )
            
            # Open the generated file and save it to the model's FileField
            with open(pdf_path, 'rb') as f:
                tailored.pdf_file.save(f"resume_{tailored.id}.pdf", File(f))
                tailored.save()
                
            # Clean up temp file
            try:
                os.remove(pdf_path)
            except OSError:
                pass
                
            return Response({'id': tailored.id}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadView(views.APIView):
    permission_classes = [AllowAny]  # Temporarily disable auth
    def get(self, request, pk, *args, **kwargs):
        try:
            tailored = TailoredResume.objects.get(id=pk)
        except TailoredResume.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        file = tailored.pdf_file
        if not file:
            return Response({'error': 'PDF not generated'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Return absolute URL so frontend can download from correct port
        return Response({'download_url': request.build_absolute_uri(file.url)}, status=status.HTTP_200_OK)
