# Gemini API Setup Instructions

## Issue Found

Your Gemini API key is valid, but the **Generative Language API is not enabled** in your Google Cloud project.

## How to Fix (2 minutes)

### Step 1: Enable the API

1. Visit this link (opens in your Google Cloud Console):
   **https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com**

2. Make sure you're signed in with the same Google account you used to create the API key

3. Click the blue **"ENABLE"** button

4. Wait 10-30 seconds for it to activate

### Step 2: Test Again

Once enabled, run this test:

```bash
cd backend
python test_gemini.py
```

You should see output like:
```
SUCCESS! Extracted keywords:
============================================================
1. Python
2. Django
3. React
4. PostgreSQL
5. Redis
...
```

## Alternative: Use Ollama (No Cloud Setup)

If you'd prefer to skip the cloud setup completely, you can use Ollama locally (100% free, runs on your PC):

### Install Ollama:
1. Download from: https://ollama.ai/download
2. Install the application
3. Open terminal and run:
   ```bash
   ollama pull llama3
   ollama serve
   ```

### Update .env:
```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Test:
```bash
cd backend
python test_gemini.py  # Will use Ollama instead
```

## Which Should You Use?

**For Cloud Deployment (Railway/Render):** 
- ✅ Enable Gemini API (best option)
- API calls work from anywhere
- Fast responses (1-2 seconds)

**For Local Testing:**
- ✅ Use Ollama (no cloud setup needed)
- Runs on your computer
- Complete privacy
- Slower first request (~5-10 seconds)

## Next Steps

1. **Enable the Generative Language API** using the link above
2. Run `python test_gemini.py` to verify
3. Add to your `.env` file:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSyA-iT2RJh7EkJXHB-yMxWMANxvN0RuOCQU
   ```
4. Test the Plannr flow!
