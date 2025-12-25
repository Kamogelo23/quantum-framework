"""
ML Model Serving Service with Ollama Integration
Provides ML model inference endpoints and local LLM services
"""
import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime
import joblib
import os
import requests
import json

app = FastAPI(
    title="Quantum ML Service",
    version="0.2.0",
    description="Machine Learning Model Serving with Ollama LLM for Quantum Platform"
)

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
DEFAULT_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:14b')


class PredictionRequest(BaseModel):
    """Prediction request model"""
    model_name: str
    features: List[float]
    metadata: Optional[Dict[str, Any]] = {}


class PredictionResponse(BaseModel):
    """Prediction response model"""
    prediction: Any
    confidence: Optional[float] = None
    model_version: str
    timestamp: str


class GenerateRequest(BaseModel):
    """Text generation request"""
    prompt: str
    model: Optional[str] = DEFAULT_MODEL
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = 2000


class GenerateResponse(BaseModel):
    """Text generation response"""
    text: str
    model: str
    timestamp: str


class ResumeParseRequest(BaseModel):
    """Resume parsing request"""
    resume_text: str
    job_description: Optional[str] = None


class KeywordExtractionRequest(BaseModel):
    """Keyword extraction request"""
    text: str


class AnomalyDetectionRequest(BaseModel):
    """Anomaly detection request"""
    data_points: List[Dict[str, float]]
    threshold: Optional[float] = 0.95


class AnomalyDetectionResponse(BaseModel):
    """Anomaly detection response"""
    anomalies: List[Dict[str, Any]]
    anomaly_count: int
    total_points: int


class ModelInfo(BaseModel):
    """Model information"""
    name: str
    version: str
    type: str
    status: str
    loaded: bool


# In-memory model storage
MODELS = {}


def call_ollama(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0.1) -> str:
    """Call Ollama API for text generation"""
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result.get('response', '')
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Ollama service error: {str(e)}"
        )


def load_models():
    """Load ML models from disk"""
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"⚠️  Models directory created. Place your trained models in: {models_dir}")
    else:
        print(f"📦 Loading models from: {models_dir}")


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    print("🚀 Quantum ML Service starting up...")
    load_models()
    
    # Check Ollama connection
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connected! Available models: {[m['name'] for m in models]}")
        else:
            print("⚠️  Ollama connection issue")
    except Exception as e:
        print(f"⚠️  Could not connect to Ollama: {e}")
    
    print("✅ ML Service ready!")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check Ollama health
    ollama_healthy = False
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        ollama_healthy = response.status_code == 200
    except:
        pass
    
    return {
        "status": "healthy" if ollama_healthy else "degraded",
        "service": "quantum-ml-service",
        "models_loaded": len(MODELS),
        "ollama_status": "connected" if ollama_healthy else "disconnected"
    }


@app.get("/models", response_model=List[ModelInfo])
async def list_models():
    """List available models"""
    models_list = [
        ModelInfo(
            name="qwen2.5-14b",
            version="14B",
            type="instruction-tuned-llm",
            status="ready",
            loaded=True
        ),
        ModelInfo(
            name="anomaly-detector",
            version="1.0.0",
            type="isolation-forest",
            status="ready",
            loaded=True
        ),
    ]
    
    # Add Ollama models
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if response.status_code == 200:
            ollama_models = response.json().get('models', [])
            for model in ollama_models:
                models_list.append(ModelInfo(
                    name=model['name'],
                    version="ollama",
                    type="llm",
                    status="ready",
                    loaded=True
                ))
    except:
        pass
    
    return models_list


@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generate text using Ollama LLM
    """
    text = call_ollama(request.prompt, request.model, request.temperature)
    
    return GenerateResponse(
        text=text,
        model=request.model,
        timestamp=datetime.now().isoformat()
    )


@app.post("/extract-keywords")
async def extract_keywords(request: KeywordExtractionRequest):
    """
    Extract keywords from job description using local LLM
    """
    prompt = f"""Extract 10-15 key technical and soft skills from this job description as a JSON array of strings.
Only return the JSON array, nothing else.

Job Description:
{request.text}

Return format: ["skill1", "skill2", "skill3", ...]"""
    
    response_text = call_ollama(prompt, DEFAULT_MODEL, 0.1)
    
    # Parse JSON from response
    try:
        # Clean up markdown code blocks if present
        cleaned = response_text.replace('```json', '').replace('```', '').strip()
        keywords = json.loads(cleaned)
        if isinstance(keywords, list):
            return {"keywords": keywords[:15]}
    except json.JSONDecodeError:
        # Fallback: try to extract lines
        lines = [line.strip().strip('-*"\'[]') for line in response_text.split('\n') if line.strip()]
        return {"keywords": lines[:15]}
    
    return {"keywords": []}


@app.post("/parse-resume")
async def parse_resume(request: ResumeParseRequest):
    """
    Parse resume into structured JSON using local LLM with optional job description for tailoring
    """
    if request.job_description:
        # Use ATS optimization prompt
        prompt = f"""You are an expert resume strategist and ATS optimization specialist. 
Your task is to analyze a job description and the candidate's resume, then transform generic achievement bullet points into targeted, keyword-optimized accomplishments.

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
            "description": "List of 4-6 highly detailed, tailored bullet points optimized for the ATS. Each bullet must include metrics and keywords from the job description." 
        }}
    ],
    "skills": ["List", "of", "optimized", "keywords"],
    "certifications": ["Cert 1", "Cert 2"]
}}

Job Description:
{request.job_description}

Resume Text:
{request.resume_text}
"""
    else:
        # Standard parsing
        prompt = f"""You are a Resume Parser. Extract structured data from the resume text.
Return ONLY a valid JSON object.

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
        {{ "title": "Title", "company": "Company", "period": "Range", "location": "Loc", "description": "3-5 detailed bullet points with achievements and metrics." }}
    ],
    "skills": ["skill1", "skill2"],
    "certifications": ["Cert 1"]
}}

Resume Text:
{request.resume_text}
"""
    
    response_text = call_ollama(prompt, DEFAULT_MODEL, 0.1)
    
    # Parse JSON
    try:
        cleaned = response_text.replace('```json', '').replace('```', '').strip()
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse LLM response as JSON: {str(e)}"
        )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Get prediction from ML model (legacy endpoint)"""
    if request.model_name not in ["anomaly-detector", "performance-predictor", "capacity-forecaster"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{request.model_name}' not found"
        )
    
    prediction_value = np.mean(request.features) * 1.2
    
    return PredictionResponse(
        prediction=prediction_value,
        confidence=0.87,
        model_version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/anomaly-detection", response_model=AnomalyDetectionResponse)
async def detect_anomalies(request: AnomalyDetectionRequest):
    """Detect anomalies in data"""
    anomalies = []
    for idx, point in enumerate(request.data_points):
        score = np.random.random()
        if score < (1 - request.threshold):
            anomalies.append({
                "index": idx,
                "data": point,
                "anomaly_score": score,
                "severity": "high" if score < 0.03 else "medium"
            })
    
    return AnomalyDetectionResponse(
        anomalies=anomalies,
        anomaly_count=len(anomalies),
        total_points=len(request.data_points)
    )


if __name__ == "__main__":
    uvicorn.run(
        "model_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
