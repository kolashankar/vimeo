"""
Simple web interface for ViMax
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import sys
from datetime import datetime
import logging

# Add parent directory to path
sys.path.insert(0, '/app')

app = FastAPI(title="ViMax Web Interface")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store job status
jobs = {}

class IdeaRequest(BaseModel):
    idea: str
    user_requirement: str = "For adults, do not exceed 3 scenes."
    style: str = "Realistic"

class ScriptRequest(BaseModel):
    script: str
    user_requirement: str = "Fast-paced with no more than 15 shots."
    style: str = "Anime Style"

class StatusResponse(BaseModel):
    chat_available: bool
    image_available: bool
    video_available: bool
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ViMax - AI Video Generation</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            .status-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .status-item {
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .status-available {
                background: #d4edda;
                color: #155724;
            }
            .status-unavailable {
                background: #fff3cd;
                color: #856404;
            }
            .form-section {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .form-section h2 {
                color: #667eea;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
            }
            textarea, input {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                font-family: inherit;
                transition: border-color 0.3s;
            }
            textarea:focus, input:focus {
                outline: none;
                border-color: #667eea;
            }
            textarea {
                min-height: 150px;
                resize: vertical;
            }
            .button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
            }
            .button:hover {
                transform: translateY(-2px);
            }
            .button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .alert {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .alert-warning {
                background: #fff3cd;
                color: #856404;
                border-left: 4px solid #ffc107;
            }
            .alert-info {
                background: #d1ecf1;
                color: #0c5460;
                border-left: 4px solid #17a2b8;
            }
            .alert-danger {
                background: #f8d7da;
                color: #721c24;
                border-left: 4px solid #dc3545;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎬 ViMax</h1>
                <p>AI-Powered Video Generation Platform</p>
            </div>

            <div class="status-card">
                <h2>📊 System Status</h2>
                <div id="statusContent" class="status-grid">
                    <div class="status-item">Loading...</div>
                </div>
            </div>

            <div id="quotaWarning" class="alert alert-warning" style="display: none;">
                <strong>⚠️ Image Generation Quota Exhausted</strong><br>
                Your API key has hit the free tier limit. Enable billing at 
                <a href="https://aistudio.google.com/app/billing" target="_blank">Google AI Studio</a>
                or wait ~24 hours for reset.
            </div>

            <div class="form-section">
                <h2>💡 Idea to Video</h2>
                <p style="margin-bottom: 20px; color: #666;">
                    Describe your idea and let AI transform it into a complete video story.
                </p>
                
                <form id="ideaForm">
                    <div class="form-group">
                        <label for="idea">Your Idea *</label>
                        <textarea id="idea" placeholder="Describe your video idea... (e.g., A cat and dog become best friends and go on an adventure)" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="ideaRequirement">Requirements</label>
                        <input type="text" id="ideaRequirement" placeholder="E.g., For adults, do not exceed 3 scenes" value="For adults, do not exceed 3 scenes.">
                    </div>
                    
                    <div class="form-group">
                        <label for="ideaStyle">Style</label>
                        <input type="text" id="ideaStyle" placeholder="E.g., Realistic, Cartoon, Anime" value="Realistic">
                    </div>
                    
                    <button type="submit" class="button">Generate Video from Idea</button>
                </form>
                
                <div id="ideaLoading" class="loading">
                    <div class="spinner"></div>
                    <p>Generating your video... This may take several minutes.</p>
                </div>
            </div>

            <div class="form-section">
                <h2>📝 Script to Video</h2>
                <p style="margin-bottom: 20px; color: #666;">
                    Provide a screenplay and generate a video from it.
                </p>
                
                <form id="scriptForm">
                    <div class="form-group">
                        <label for="script">Your Script *</label>
                        <textarea id="script" placeholder="EXT. LOCATION - TIME&#10;Character descriptions...&#10;CHARACTER: Dialog here" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="scriptRequirement">Requirements</label>
                        <input type="text" id="scriptRequirement" placeholder="E.g., Fast-paced with no more than 15 shots" value="Fast-paced with no more than 15 shots.">
                    </div>
                    
                    <div class="form-group">
                        <label for="scriptStyle">Style</label>
                        <input type="text" id="scriptStyle" placeholder="E.g., Anime Style, Cinematic" value="Anime Style">
                    </div>
                    
                    <button type="submit" class="button">Generate Video from Script</button>
                </form>
                
                <div id="scriptLoading" class="loading">
                    <div class="spinner"></div>
                    <p>Generating your video... This may take several minutes.</p>
                </div>
            </div>

            <div id="result" class="alert alert-info" style="display: none;"></div>
        </div>

        <script>
            // Check API status on load
            async function checkStatus() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    
                    const statusHtml = `
                        <div class="status-item ${data.chat_available ? 'status-available' : 'status-unavailable'}">
                            <h3>${data.chat_available ? '✅' : '❌'} Chat Model</h3>
                            <p>${data.chat_available ? 'Available' : 'Unavailable'}</p>
                        </div>
                        <div class="status-item ${data.image_available ? 'status-available' : 'status-unavailable'}">
                            <h3>${data.image_available ? '✅' : '⚠️'} Image Generation</h3>
                            <p>${data.image_available ? 'Available' : 'Quota Limit'}</p>
                        </div>
                        <div class="status-item status-unavailable">
                            <h3>⏳ Video Generation</h3>
                            <p>Ready (untested)</p>
                        </div>
                    `;
                    
                    document.getElementById('statusContent').innerHTML = statusHtml;
                    
                    if (!data.image_available) {
                        document.getElementById('quotaWarning').style.display = 'block';
                    }
                } catch (error) {
                    document.getElementById('statusContent').innerHTML = 
                        '<div class="status-item status-unavailable"><p>Error checking status</p></div>';
                }
            }
            
            checkStatus();
            
            // Handle Idea Form
            document.getElementById('ideaForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const button = e.target.querySelector('button');
                const loading = document.getElementById('ideaLoading');
                const result = document.getElementById('result');
                
                button.disabled = true;
                loading.style.display = 'block';
                result.style.display = 'none';
                
                try {
                    const response = await fetch('/api/generate/idea', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            idea: document.getElementById('idea').value,
                            user_requirement: document.getElementById('ideaRequirement').value,
                            style: document.getElementById('ideaStyle').value
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        result.className = 'alert alert-info';
                        result.innerHTML = `<strong>✅ Success!</strong><br>${data.message}`;
                    } else {
                        result.className = 'alert alert-danger';
                        result.innerHTML = `<strong>❌ Error:</strong><br>${data.detail}`;
                    }
                    result.style.display = 'block';
                } catch (error) {
                    result.className = 'alert alert-danger';
                    result.innerHTML = `<strong>❌ Error:</strong><br>${error.message}`;
                    result.style.display = 'block';
                } finally {
                    button.disabled = false;
                    loading.style.display = 'none';
                }
            });
            
            // Handle Script Form
            document.getElementById('scriptForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const button = e.target.querySelector('button');
                const loading = document.getElementById('scriptLoading');
                const result = document.getElementById('result');
                
                button.disabled = true;
                loading.style.display = 'block';
                result.style.display = 'none';
                
                try {
                    const response = await fetch('/api/generate/script', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            script: document.getElementById('script').value,
                            user_requirement: document.getElementById('scriptRequirement').value,
                            style: document.getElementById('scriptStyle').value
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        result.className = 'alert alert-info';
                        result.innerHTML = `<strong>✅ Success!</strong><br>${data.message}`;
                    } else {
                        result.className = 'alert alert-danger';
                        result.innerHTML = `<strong>❌ Error:</strong><br>${data.detail}`;
                    }
                    result.style.display = 'block';
                } catch (error) {
                    result.className = 'alert alert-danger';
                    result.innerHTML = `<strong>❌ Error:</strong><br>${error.message}`;
                    result.style.display = 'block';
                } finally {
                    button.disabled = false;
                    loading.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/status")
async def check_status():
    """Check API availability"""
    from google import genai
    from google.genai import types
    
    api_key = "AIzaSyBY3hgYVQsuko7xcBZOhlSCvw1KIxhvdH4"
    client = genai.Client(api_key=api_key)
    
    # Check chat model
    chat_available = False
    try:
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-lite-preview-09-2025',
            contents='test'
        )
        chat_available = True
    except:
        pass
    
    # Check image generation
    image_available = False
    try:
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-image',
            contents=['test'],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="16:9"),
            ),
        )
        image_available = True
    except:
        pass
    
    return StatusResponse(
        chat_available=chat_available,
        image_available=image_available,
        video_available=False,  # Will be tested during actual generation
        message="System ready" if chat_available else "Chat model unavailable"
    )

async def run_idea2video(idea: str, user_requirement: str, style: str):
    """Run idea2video pipeline"""
    try:
        from pipelines.idea2video_pipeline import Idea2VideoPipeline
        
        pipeline = Idea2VideoPipeline.init_from_config(
            config_path="/app/configs/idea2video.yaml"
        )
        await pipeline(idea=idea, user_requirement=user_requirement, style=style)
        return True, "Video generated successfully! Check .working_dir/idea2video/"
    except Exception as e:
        logging.error(f"Idea2Video error: {e}")
        return False, str(e)

async def run_script2video(script: str, user_requirement: str, style: str):
    """Run script2video pipeline"""
    try:
        from pipelines.script2video_pipeline import Script2VideoPipeline
        
        pipeline = Script2VideoPipeline.init_from_config(
            config_path="/app/configs/script2video.yaml"
        )
        await pipeline(script=script, user_requirement=user_requirement, style=style)
        return True, "Video generated successfully! Check .working_dir/script2video/"
    except Exception as e:
        logging.error(f"Script2Video error: {e}")
        return False, str(e)

@app.post("/api/generate/idea")
async def generate_from_idea(request: IdeaRequest, background_tasks: BackgroundTasks):
    """Generate video from idea"""
    job_id = f"idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    jobs[job_id] = {"status": "processing", "message": "Processing..."}
    
    # Run in background
    success, message = await run_idea2video(request.idea, request.user_requirement, request.style)
    
    if success:
        return {"message": message, "job_id": job_id}
    else:
        raise HTTPException(status_code=500, detail=f"Generation failed: {message}")

@app.post("/api/generate/script")
async def generate_from_script(request: ScriptRequest, background_tasks: BackgroundTasks):
    """Generate video from script"""
    job_id = f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    jobs[job_id] = {"status": "processing", "message": "Processing..."}
    
    # Run in background
    success, message = await run_script2video(request.script, request.user_requirement, request.style)
    
    if success:
        return {"message": message, "job_id": job_id}
    else:
        raise HTTPException(status_code=500, detail=f"Generation failed: {message}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
