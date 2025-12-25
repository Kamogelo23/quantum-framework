"""
Test script to verify Gemini API key works for keyword extraction
"""
import os
import sys

# Set the API key for testing
os.environ['AI_PROVIDER'] = 'gemini'
os.environ['GEMINI_API_KEY'] = 'AIzaSyA-iT2RJh7EkJXHB-yMxWMANxvN0RuOCQU'

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the keyword extractor
try:
    from apps.plannr.services.keyword_extractor import extract_keywords
    
    print("Testing Gemini API key...")
    print("=" * 60)
    
    test_job = """
    Senior Python Developer
    
    We are looking for an experienced Python developer with strong Django 
    and React skills. The ideal candidate should have experience with 
    PostgreSQL, Redis, Docker, and REST APIs. Knowledge of machine learning 
    and cloud deployment (AWS/GCP) is a plus.
    
    Requirements:
    - 5+ years Python experience
    - Strong Django and DRF skills
    - Frontend experience with React
    - Good communication skills
    - Team player
    """
    
    print(f"Test job description:\n{test_job[:100]}...\n")
    print("Extracting keywords with Gemini...")
    print()
    
    keywords = extract_keywords(test_job)
    
    print("SUCCESS! Extracted keywords:")
    print("=" * 60)
    for i, keyword in enumerate(keywords, 1):
        print(f"{i}. {keyword}")
    
    print("\n" + "=" * 60)
    print(f"Total keywords extracted: {len(keywords)}")
    print("Your Gemini API key is working perfectly!")
    print("\nNext step: Add these lines to your .env file:")
    print("  AI_PROVIDER=gemini")
    print("  GEMINI_API_KEY=AIzaSyA-iT2RJh7EkJXHB-yMxWMANxvN0RuOCQU")
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check that your API key is correct")
    print("2. Ensure you have internet connection")
    print("3. Install requests: pip install requests")
    print("4. Visit https://aistudio.google.com/app/apikey to verify your key")
    import traceback
    traceback.print_exc()
    sys.exit(1)
