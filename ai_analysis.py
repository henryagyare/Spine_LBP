"""
AI-powered post-prediction analysis using Groq or OpenAI
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_ai_analysis(prediction, confidence_score):
    """
    Get AI-powered analysis of the prediction results.
    
    Args:
        prediction: The predicted class (e.g., "with_pain", "without_pain")
        confidence_score: The confidence score (0-1)
    
    Returns:
        str: AI-generated analysis or None if API key not configured
    """
    # Check for Groq API key first (recommended)
    groq_api_key = os.getenv('GROQ_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if groq_api_key and groq_api_key != 'your_groq_api_key_here':
        return _get_groq_analysis(prediction, confidence_score, groq_api_key)
    elif openai_api_key and openai_api_key != 'your_openai_api_key_here':
        return _get_openai_analysis(prediction, confidence_score, openai_api_key)
    else:
        return None


def _get_groq_analysis(prediction, confidence_score, api_key):
    """Get analysis using Groq API (Fast & Free)."""
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        # Create prompt for analysis
        prompt = f"""You are a medical AI assistant analyzing spinal MRI scan results. 
        
Result: {prediction.replace('_', ' ').title()}
Confidence: {confidence_score:.1%}

Provide a brief, professional analysis (2-3 sentences) covering:
1. What this result suggests
2. Recommended next steps
3. Important considerations

Keep it concise, educational, and appropriate for students learning about AI in healthcare."""

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical AI assistant providing educational analysis of diagnostic results."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",  # Fast and accurate
            temperature=0.7,
            max_completion_tokens=200,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Error getting AI analysis: {str(e)}"


def _get_openai_analysis(prediction, confidence_score, api_key):
    """Get analysis using OpenAI API (Alternative option)."""
    try:
        import openai
        
        openai.api_key = api_key
        
        # Create prompt for analysis
        prompt = f"""You are a medical AI assistant analyzing spinal MRI scan results. 
        
Result: {prediction.replace('_', ' ').title()}
Confidence: {confidence_score:.1%}

Provide a brief, professional analysis (2-3 sentences) covering:
1. What this result suggests
2. Recommended next steps
3. Important considerations

Keep it concise, educational, and appropriate for students learning about AI in healthcare."""

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical AI assistant providing educational analysis of diagnostic results."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Error getting AI analysis: {str(e)}"


def is_api_configured():
    """Check if AI API is configured."""
    groq_key = os.getenv('GROQ_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    groq_configured = groq_key and groq_key != 'your_groq_api_key_here'
    openai_configured = openai_key and openai_key != 'your_openai_api_key_here'
    
    return groq_configured or openai_configured


def get_api_setup_instructions():
    """Get instructions for setting up API key."""
    return """
### 🔑 AI Analysis Setup (Optional)

To enable AI-powered post-prediction analysis:

**Option 1: Groq (Recommended - Free & Fast)**
1. Visit [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (free, no credit card needed)
3. Create an API key
4. Copy `.env.example` to `.env`
5. Add your key to `.env`
6. Restart the app

**Option 2: OpenAI (ChatGPT)**
1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create an API key
3. Add to `.env` file
4. Restart the app

**File location:** `Spinal-Disease-Classifier/.env`
"""

