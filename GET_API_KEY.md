# 🔑 Get Your Groq API Key (2 Minutes)

## Quick Steps:

### 1. Visit Groq Console
👉 **https://console.groq.com/keys**

### 2. Sign Up (Free, No Credit Card)
- Click "Sign Up" or "Get Started"
- Use your email (Google/GitHub login available)
- Verify your email
- **No payment information required!**

### 3. Create API Key
- Go to "API Keys" section
- Click "Create API Key"
- Give it a name (e.g., "Spinal Classifier")
- Copy the key (starts with `gsk_...`)

### 4. Add to Your Project
```bash
cd /Users/saha/Desktop/ferno/GitHub/Spinal-Disease-Classifier

# Copy example file
cp .env.example .env

# Open .env and replace:
# GROQ_API_KEY=your_groq_api_key_here
# with your actual key:
# GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxx
```

### 5. Restart App
```bash
# Stop current app (Ctrl+C or close terminal)
# Then restart:
streamlit run main.py
```

---

## ✅ Testing

1. Upload an MRI image in the app
2. Look for **"🤖 AI-Powered Analysis"** section
3. Should see AI analysis in 1-2 seconds!

---

## 🎯 What You'll Get

The AI will provide:
- Professional medical context
- Recommended next steps
- Important considerations
- Educational insights

Example:
```
"This result suggests potential spinal discomfort. It's recommended 
to consult with a healthcare provider for comprehensive evaluation. 
Machine learning models should support, not replace, professional 
medical judgment."
```

---

## 💡 Why Groq?

✅ **FREE** - No charges, ever  
✅ **FAST** - 10-100x faster than competitors  
✅ **EASY** - No credit card needed  
✅ **POWERFUL** - Llama 3.1 70B model  

---

## 🔒 Security Note

Your API key is stored in `.env` file which is:
- ✅ NOT committed to git
- ✅ Listed in `.gitignore`
- ✅ Only on your local machine

**Never share your `.env` file!**

---

## Alternative: OpenAI

Prefer ChatGPT? See `API_SETUP.md` for OpenAI instructions.

---

**Ready? Get your key: https://console.groq.com/keys** 🚀

