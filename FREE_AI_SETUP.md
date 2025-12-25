# 🆓 100% Free AI Setup for Plannr

## Quick Start - Choose One Free Option

### ⭐ Option 1: Google Gemini (RECOMMENDED - Easiest)

**Why Gemini:**
- ✅ **Completely free** - No credit card required
- ✅ **60 requests/minute** free tier
- ✅ **Best for cloud deployment** (API-based)
- ✅ **Very capable** for keyword extraction

**Setup (2 minutes):**

1. **Get your free API key:**
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Get API Key" (or "Create API Key")
   - Sign in with Google account
   - Click "Create API key in new project"
   - **Copy the key** (starts with `AIza...`)

2. **Add to `.env` file:**
   ```bash
   cd backend
   # Create .env from example
   cp .env.example .env
   
   # Add these lines to .env:
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSy...your-key-here
   ```

3. **Test it:**
   ```bash
   python manage.py shell
   ```
   ```python
   from apps.plannr.services.keyword_extractor import extract_keywords
   keywords = extract_keywords("Senior Python Developer with Django and React experience")
   print(keywords)
   # Should output: ['Python', 'Django', 'React', 'Senior', ...]
   ```

**That's it! ✅**

---

### ⭐ Option 2: Hugging Face (Great Alternative)

**Why Hugging Face:**
- ✅ **Completely free** - No credit card
- ✅ **30,000 requests/month** free
- ✅ **Many models available**

**Setup:**

1. **Get your free token:**
   - Visit: https://huggingface.co/join
   - Sign up (free)
   - Go to: https://huggingface.co/settings/tokens
   - Click "New token"
   - Name it "plannr", select "Read" access
   - **Copy the token** (starts with `hf_...`)

2. **Add to `.env`:**
   ```env
   AI_PROVIDER=huggingface
   HUGGINGFACE_TOKEN=hf_...your-token-here
   ```

---

### ⭐ Option 3: Ollama (Best for Privacy - Runs Locally)

**Why Ollama:**
- ✅ **100% free** - runs on your computer
- ✅ **No API calls** - complete privacy
- ✅ **No internet required** after setup
- ✅ **Best for local testing**

**Setup:**

1. **Install Ollama:**
   - Windows: Download from https://ollama.ai/download
   - Run the installer

2. **Download a model:**
   ```bash
   # In terminal/PowerShell
   ollama pull llama3
   ```

3. **Start Ollama:**
   ```bash
   ollama serve
   ```
   (Keep this running in the background)

4. **Add to `.env`:**
   ```env
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   ```

**Note:** First extraction will be slower (~5-10 seconds), but completely free and private!

---

## Comparison Table

| Provider | Free? | Speed | Best For |
|----------|-------|-------|----------|
| **Gemini** ⭐ | ✅ Yes (no card) | Fast (1-2s) | **Cloud deployment** |
| **Hugging Face** | ✅ Yes (no card) | Medium (2-3s) | Alternative to Gemini |
| **Ollama** | ✅ Yes (local) | Slow (5-10s) | **Privacy, local testing** |
| Claude | ❌ Requires payment | Fast (1-2s) | If you need Claude specifically |

---

## Troubleshooting

### Gemini Errors

**"API key not valid"**
- Make sure you copied the entire key (starts with `AIza...`)
- Check there are no extra spaces in `.env`

**"Quota exceeded"**
- Free tier: 60 requests/minute
- Wait 1 minute and try again

### Hugging Face Errors

**"Model is loading"**
- Some models take 20-30 seconds to "warm up" the first time
- Try again after 30 seconds

**"Rate limit exceeded"**
- Free tier: 30,000 requests/month
- Should be plenty for testing

### Ollama Errors

**"Connection refused"**
- Make sure Ollama is running: `ollama serve`
- Check it's running on port 11434

**"Model not found"**
- Download the model: `ollama pull llama3`

---

## Recommended Setup

### For Local Development:
```env
AI_PROVIDER=ollama
# No API key needed, runs locally
```

### For Cloud Deployment (Railway/Render):
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=AIza...your-key-here
```

### For Production (if budget allows):
```env
AI_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-...your-key-here
```

---

## Next Steps

1. **Choose your provider** (Gemini recommended)
2. **Get your free API key** (2 minutes)
3. **Add to `.env` file**
4. **Test the flow:**
   ```bash
   python manage.py runserver
   # Visit http://localhost:4200/plannr
   ```

All of these are **100% free** with no credit card required! 🎉
