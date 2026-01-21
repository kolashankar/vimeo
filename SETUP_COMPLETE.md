# 🎬 ViMax - Agentic Video Generation

## ✅ Setup Status: COMPLETE

Your ViMax installation is ready! The project uses AI to convert ideas, scripts, and novels into complete videos.

---

## 🔑 Current Configuration

**API Key**: `AIzaSyBY3hgYVQsuko7xcBZOhlSCvw1KIxhvdH4`

**Services Configured**:
- ✅ **Chat Model**: Gemini 2.5 Flash Lite (WORKING)
- ⚠️  **Image Generator**: Nano Banana (QUOTA LIMIT - needs billing or 24hr wait)
- ⏳ **Video Generator**: Veo 3.1 (untested - will check during first run)

---

## 🚀 Quick Start

### Option 1: Interactive Menu
```bash
cd /app
./run_vimax.sh
```

### Option 2: Direct Commands

**Check API Status:**
```bash
cd /app
source .venv/bin/activate
python check_status.py
```

**Run Idea to Video:**
```bash
cd /app
source .venv/bin/activate
python main_idea2video.py
```

**Run Script to Video:**
```bash
cd /app
source .venv/bin/activate
python main_script2video.py
```

---

## 📝 How It Works

### 1. Idea2Video
Edit `/app/main_idea2video.py` to customize your idea:
```python
idea = """
Your creative idea here...
"""
user_requirement = """
For adults, do not exceed 3 scenes.
"""
style = "Realistic, warm feel"
```

### 2. Script2Video
Edit `/app/main_script2video.py` to use your screenplay:
```python
script = """
EXT. LOCATION - TIME
Your scene description...
CHARACTER: Dialog here
"""
user_requirement = """
Fast-paced with no more than 15 shots.
"""
style = "Anime Style"
```

---

## ⚠️ Current Issue: Image Generation Quota

Your API key has hit the **free tier quota limit** for image generation. This is Google's rate limit, not an error with ViMax.

### Solutions:

**Option 1: Enable Billing (Immediate)**
- Visit: https://aistudio.google.com/app/billing
- Add payment method to use pay-as-you-go pricing

**Option 2: Wait for Reset (~24 hours)**
- Free tier quotas reset daily
- Check status with: `python check_status.py`

**Option 3: New API Key**
- Generate new key: https://aistudio.google.com/app/apikey
- Update configs manually or ask me to help

---

## 📂 Project Structure

```
/app/
├── main_idea2video.py          # Main script for idea→video
├── main_script2video.py        # Main script for script→video
├── check_status.py             # API status checker
├── run_vimax.sh                # Interactive launcher
├── configs/
│   ├── idea2video.yaml         # Idea2Video configuration
│   └── script2video.yaml       # Script2Video configuration
├── pipelines/                  # Processing pipelines
├── agents/                     # AI agents
├── tools/                      # Generator tools
└── .working_dir/              # Output directory (created on first run)
```

---

## 🎯 Features

- **💡 Idea2Video**: Transform raw ideas into complete video stories
- **📝 Script2Video**: Convert screenplays into videos
- **🎨 Multi-Agent System**: Automated scriptwriting, storyboarding, character design
- **🔄 Consistency**: Maintains character and scene consistency across shots
- **⚡ Parallel Processing**: Efficient multi-shot generation

---

## 🐛 Troubleshooting

### "Web server returned an unknown error"
- ✅ **FIXED**: Updated to correct API configuration
- Chat model is now working properly

### "Quota exhausted" for images
- This is expected with free tier
- Enable billing or wait for daily reset

### Other Issues
Run status check:
```bash
python check_status.py
```

---

## 📚 Documentation

- Official ViMax Docs: Check `/app/readme.md`
- Google AI Studio: https://aistudio.google.com
- Rate Limits Info: https://ai.google.dev/gemini-api/docs/rate-limits

---

## 🎉 You're All Set!

The project is **fully configured** and ready to generate videos once the image generation quota is available.

Try running:
```bash
./run_vimax.sh
```

Or test individual components:
```bash
python check_status.py
```
