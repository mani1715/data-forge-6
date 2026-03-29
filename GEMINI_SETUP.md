# 🤖 DataForge - AI-Powered Data Cleaning

## Setting Up Gemini AI API Key

DataForge uses **Google's Gemini AI** for intelligent data cleaning. You need to provide your own Gemini API key.

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated API key

### Step 2: Add API Key to Your Project

1. Navigate to `/app/backend/`
2. Open `.env` file (or copy from `.env.example`)
3. Replace `your-gemini-api-key-here` with your actual key:

```env
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

4. Save the file

### Step 3: Restart the Backend

```bash
sudo supervisorctl restart backend
```

### Verification

Test if AI is working:
```bash
curl http://localhost:8001/health
```

You should see: `{"status": "healthy"}`

---

## 🧹 AI-Powered Features

All cleaning operations use Gemini AI:

- ✅ **Clean Missing Values** - AI analyzes patterns and recommends best imputation strategy
- ✅ **Remove Duplicates with AI** - AI detects duplicate patterns across columns
- ✅ **Remove Outliers with AI** - AI analyzes numeric distributions for outlier detection
- ✅ **Clean Text Data with AI** - AI identifies text patterns and quality issues

---

## 🔒 Security Note

- Never commit your `.env` file to Git
- Keep your API key private
- The `.env` file is already in `.gitignore`

---

## 💰 API Costs

Gemini AI has a free tier:
- **Free tier:** 15 requests per minute
- **Cost:** Free for most use cases
- [See pricing](https://ai.google.dev/pricing)

---

## 🚀 Deployment

When deploying, make sure to:
1. Add `GEMINI_API_KEY` to your environment variables
2. Set `FLASK_ENV=production`
3. Set `FLASK_DEBUG=False`

---

## ❓ Troubleshooting

**AI not working?**
- Check if `GEMINI_API_KEY` is set in `.env`
- Verify the API key is valid
- Check backend logs: `tail -f /var/log/supervisor/backend.err.log`

**Rate limit errors?**
- Wait a few seconds between requests
- Gemini free tier: 15 requests/minute

---

## 📚 Documentation

- [Gemini AI Documentation](https://ai.google.dev/docs)
- [Get API Key](https://aistudio.google.com/apikey)

