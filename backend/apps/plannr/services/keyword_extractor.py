import os
import requests
import json
from django.conf import settings

# AI Provider Configuration
AI_PROVIDER = os.getenv('AI_PROVIDER', 'local')  # Options: 'gemini', 'local', 'ollama', 'claude'

# API Keys/Tokens
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or 'AIzaSyA-iT2RJh7EkJXHB-yMxWMANxvN0RuOCQU'  # Fallback for local dev
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# Local ML Service Configuration
ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://ml-service:8001')

def extract_keywords_local(text: str) -> list:
    """Extract keywords using local ml-service (Qwen 2.5)"""
    try:
        url = f"{ML_SERVICE_URL}/extract-keywords"
        payload = {"text": text}
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('keywords', [])
    except Exception as e:
        print(f"[Local ML Service Error]: {str(e)}")
        raise

def extract_keywords_gemini(text: str) -> list:
    """Extract keywords using Google Gemini (FREE - No credit card required)"""
    if not GEMINI_API_KEY:
        raise RuntimeError('GEMINI_API_KEY not configured')
    
    # Use gemini-2.5-flash (available in free tier)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""Extract 10-15 key technical and soft skills from this job description as a JSON array of strings.
Only return the JSON array, nothing else.

Job Description:
{text}

Return format: ["skill1", "skill2", "skill3", ...]"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
    response.raise_for_status()
    
    result = response.json()
    if 'candidates' in result and len(result['candidates']) > 0:
        text_response = result['candidates'][0]['content']['parts'][0]['text']
        # Try to parse as JSON
        try:
            # Remove markdown code blocks if present
            text_response = text_response.replace('```json', '').replace('```', '').strip()
            keywords = json.loads(text_response)
            return keywords if isinstance(keywords, list) else []
        except json.JSONDecodeError:
            # Fallback: split by commas
            return [k.strip().strip('"\'') for k in text_response.split(',') if k.strip()]
    return []

def extract_keywords_huggingface(text: str) -> list:
    """Extract keywords using Hugging Face (FREE - No credit card required)"""
    if not HUGGINGFACE_TOKEN:
        raise RuntimeError('HUGGINGFACE_TOKEN not configured')
    
    # Using Mistral-7B-Instruct (free tier)
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""[INST] Extract 10-15 key technical and soft skills from this job description. Return only a JSON array of strings.

Job Description:
{text}

Return format: ["skill1", "skill2", "skill3", ...] [/INST]"""
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.1
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        text_response = result[0].get('generated_text', '')
        # Extract JSON from response
        try:
            # Find JSON array in response
            start = text_response.find('[')
            end = text_response.rfind(']') + 1
            if start != -1 and end != 0:
                keywords = json.loads(text_response[start:end])
                return keywords if isinstance(keywords, list) else []
        except:
            pass
    return []

def extract_keywords_ollama(text: str) -> list:
    """Extract keywords using Ollama (FREE - Local, no internet required)"""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    
    prompt = f"""Extract 10-15 key technical and soft skills from this job description as a JSON array.
Return ONLY the JSON array, nothing else.

Job Description:
{text}

Format: ["skill1", "skill2", ...]"""
    
    payload = {
        "model": "llama3",  # or "mistral", "phi", etc.
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        text_response = result.get('response', '')
        
        # Parse JSON from response
        try:
            text_response = text_response.replace('```json', '').replace('```', '').strip()
            keywords = json.loads(text_response)
            return keywords if isinstance(keywords, list) else []
        except:
            # Fallback: split by newlines/commas
            lines = [line.strip().strip('-*"\'[]') for line in text_response.split('\n') if line.strip()]
            return [k for k in lines if k and len(k) < 50][:15]
    except requests.exceptions.ConnectionError:
        raise RuntimeError('Ollama is not running. Start it with: ollama serve')
    except Exception as e:
        raise RuntimeError(f'Ollama error: {str(e)}')

def extract_keywords_claude(text: str) -> list:
    """Extract keywords using Claude (PAID - Requires credit card)"""
    if not CLAUDE_API_KEY:
        raise RuntimeError('CLAUDE_API_KEY not configured')
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json',
    }
    
    prompt = f"Extract 10-15 key technical and soft skills from this job description as a JSON array of strings.\n\nJob Description:\n{text}"
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 200,
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    
    if 'content' in result and len(result['content']) > 0:
        text_response = result['content'][0]['text']
        try:
            text_response = text_response.replace('```json', '').replace('```', '').strip()
            keywords = json.loads(text_response)
            return keywords if isinstance(keywords, list) else []
        except:
            return []
    return []

    return []

def extract_keywords_simple(text: str) -> list:
    """Extract keywords using simple rule-based logic (Offline fallback)"""
    # Basic list of common tech keywords to look for
    common_skills = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'django', 'flask', 'fastapi', 'spring', 'react', 'angular', 'vue',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'ci/cd',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis',
        'machine learning', 'ai', 'data science', 'nlp', 'pytorch', 'tensorflow',
        'communication', 'leadership', 'agile', 'scrum', 'problem solving'
    ]
    
    found_keywords = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill in text_lower:
            found_keywords.append(skill.title())
            
    # If few found, add some generics based on text content
    if len(found_keywords) < 5:
        # Simple heuristic: capitalized words that aren't stop words (very basic)
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 4:
                clean_word = word.strip('.,()[]')
                if clean_word not in found_keywords:
                    found_keywords.append(clean_word)
                    
    return found_keywords[:15]

def extract_keywords(text: str) -> list:
    """
    Main function to extract keywords using the configured AI provider.
    
    Providers (set via AI_PROVIDER env var):
    - 'gemini': Google Gemini (FREE - Recommended)
    - 'huggingface': Hugging Face Inference API (FREE)
    - 'ollama': Local Ollama (FREE - Most private)
    - 'claude': Anthropic Claude (PAID)
    """
    providers = {
        'gemini': extract_keywords_gemini,
        'huggingface': extract_keywords_huggingface,
        'ollama': extract_keywords_ollama,
        'claude': extract_keywords_claude,
        'simple': extract_keywords_simple,
        'local': extract_keywords_local,
    }
    
    provider_func = providers.get(AI_PROVIDER)
    if not provider_func:
        raise RuntimeError(f'Unknown AI provider: {AI_PROVIDER}. Use: gemini, huggingface, ollama, or claude')
    
    try:
        keywords = provider_func(text)
        return keywords[:15]  # Limit to 15 keywords
    except Exception as e:
        print(f"[Keyword Extraction Error] Provider: {AI_PROVIDER}, Error: {str(e)}")
        raise

def parse_resume_data(text: str, job_description: str = None) -> dict:
    """
    Parses and optionally tailors resume data using configured AI provider.
    If job_description is provided, it uses an advanced ATS optimization prompt.
    """
    try:
        if AI_PROVIDER == 'local':
            return parse_resume_data_local(text, job_description)
        elif AI_PROVIDER == 'gemini':
            return parse_resume_data_gemini(text, job_description)
        else:
            print(f"[WARNING] Unsupported provider for resume parsing: {AI_PROVIDER}")
            return {}
    except Exception as e:
        print(f"[Resume Parsing Error]: {str(e)}")
        return {}


def parse_resume_data_local(text: str, job_description: str = None) -> dict:
    """
    Parse resume using local ml-service (Qwen 2.5)
    """
    try:
        url = f"{ML_SERVICE_URL}/parse-resume"
        payload = {
            "resume_text": text,
            "job_description": job_description
        }
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[Local ML Service Error]: {str(e)}")
        raise


def parse_resume_data_gemini(text: str, job_description: str = None) -> dict:
    """
    Parses and optionally tailors resume data using Gemini.
    If job_description is provided, it uses an advanced ATS optimization prompt.
    """
    if not GEMINI_API_KEY:
        print("[WARNING] GEMINI_API_KEY not configured, returning empty data")
        return {}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    if job_description:
        # Advanced ATS Optimization Prompt
        prompt = f"""You are an expert resume strategist and ATS optimization specialist. 
Your task is to analyze a job description and the candidate's resume, then transform generic achievement bullet points into targeted, keyword-optimized accomplishments.

**PHASE 1: JOB DESCRIPTION ANALYSIS**
Analyze the provided job description for required hard skills, soft skills, quantifiable requirements, and core competencies.

**PHASE 2: KEYWORD EXTRACTION & MAPPING**
Identify primary, secondary, and tertiary keywords from the job description to target in the resume.

**PHASE 3: ACHIEVEMENT TRANSFORMATION**
Transform the candidate's experience using this formula:
Before: [Generic accomplishment]
After: [Keyword-optimized version]
Rules:
- Direct Keyword Integration: use JD terminology
- Metric Alignment: match metrics to JD scale
- Responsibility Mapping: align experience with JD
- Value Proposition Reframing: reposition outcomes

**PHASE 4: MEASURABLE OUTCOME ENHANCEMENT**
Ensure each bullet point includes scale matching (users, data volume), metric hierarchy (financial, performance, scale), and action verb alignment.

**TASK:**
Extract and transform the resume content based on the job description.
Return ONLY a valid JSON object with this structure:
{{
    "name": "Candidate Name",
    "email": "email",
    "phone": "phone",
    "location": "City, Country",
    "linkedin": "linkedin url (if found)",
    "github": "github url (if found)",
    "education": [
        {{ "degree": "Degree", "institution": "University", "year": "Year" }}
    ],
    "experience": [
        {{
            "title": "Job Title",
            "company": "Company",
            "period": "Date Range",
            "location": "Location",
            "description": "List of 4-6 highly detailed, tailored bullet points (sentences) optimized for the ATS. Each bullet must be comprehensive and include metrics." 
        }}
    ],
    "skills": ["List", "of", "optimized", "keywords", "matches"],
    "certifications": ["Cert 1", "Cert 2"]
}}

Job Description:
--BEGIN JD--
{job_description}
--END JD--

Resume Text:
--BEGIN RESUME--
{text}
--END RESUME--
"""
    else:
        # Standard Parsing Prompt (No JD) -> Updated to be more detailed
        prompt = f"""You are a Resume Parser. Extract structured data from the resume text.
Return ONLY a valid JSON object.

Instructions:
- description: Provide 3-5 detailed bullet points for each role, distinct strings separated by newlines or joined as a full text block. Focus on achievements.
- skills: Extract technical and soft skills.

Structure:
{{
    "name": "Name",
    "email": "email",
    "phone": "phone",
    "location": "City, Country",
    "linkedin": "url",
    "github": "url",
    "education": [{{ "degree": "Degree", "institution": "University", "year": "Year" }}],
    "experience": [
        {{ "title": "Title", "company": "Company", "period": "Range", "location": "Loc", "description": "3-5 detailed bullet points. Do not summarize briefly." }}
    ],
    "skills": ["skill1", "skill2"],
    "certifications": ["Cert 1"]
}}

Resume Text:
{text}
"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            # Clean up markdown
            text_response = text_response.replace('```json', '').replace('```', '').strip()
            data = json.loads(text_response)
            return data
    except Exception as e:
        print(f"[Resume Parsing Error]: {str(e)}")
        # import traceback
        # traceback.print_exc()
        
    return {}
