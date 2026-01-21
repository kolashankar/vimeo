"""
ViMax Backend Server - FastAPI Application
AI-Powered Video Generation Platform
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import os
import sys
from datetime import datetime
import logging
from typing import Optional, List, Dict
import json
from pathlib import Path

# Add backend directory to path for imports
sys.path.insert(0, '/app/backend')
sys.path.insert(0, '/app')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ViMax API",
    description="AI-Powered Video Generation Platform",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global job tracking
jobs: Dict[str, dict] = {}

# Request Models
class IdeaRequest(BaseModel):
    idea: str
    user_requirement: str = "For adults, do not exceed 3 scenes."
    style: str = "Realistic"

class ScriptRequest(BaseModel):
    script: str
    user_requirement: str = "Fast-paced with no more than 15 shots."
    style: str = "Anime Style"

# Response Models
class StatusResponse(BaseModel):
    chat_available: bool
    image_available: bool
    video_available: bool
    message: str

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: str
    working_dir: Optional[str] = None

class VideoInfo(BaseModel):
    filename: str
    path: str
    size: int
    created_at: str
    type: str

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/status")
async def check_status():
    """Check API availability and system status"""
    try:
        from google import genai
        from google.genai import types
        
        # Get API key from config
        config_path = "/app/backend/configs/idea2video.yaml"
        api_key = None
        
        if os.path.exists(config_path):
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                api_key = config.get('chat_model', {}).get('init_args', {}).get('api_key')
        
        if not api_key:
            return StatusResponse(
                chat_available=False,
                image_available=False,
                video_available=False,
                message="API key not configured"
            )
        
        client = genai.Client(api_key=api_key)
        
        # Check chat model
        chat_available = False
        try:
            response = await client.aio.models.generate_content(
                model='models/gemini-2.5-flash-lite-preview-09-2025',
                contents='test'
            )
            chat_available = True
            logger.info("Chat model check: Available")
        except Exception as e:
            logger.warning(f"Chat model check failed: {e}")
        
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
            logger.info("Image generation check: Available")
        except Exception as e:
            logger.warning(f"Image generation check failed: {e}")
        
        return StatusResponse(
            chat_available=chat_available,
            image_available=image_available,
            video_available=False,  # Will be tested during actual generation
            message="System ready" if chat_available else "Some services unavailable"
        )
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return StatusResponse(
            chat_available=False,
            image_available=False,
            video_available=False,
            message=f"Status check failed: {str(e)}"
        )

async def run_idea2video(job_id: str, idea: str, user_requirement: str, style: str):
    """Run idea2video pipeline in background"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["message"] = "Initializing pipeline..."
        logger.info(f"Job {job_id}: Starting idea2video pipeline")
        
        from backend.pipelines.idea2video_pipeline import Idea2VideoPipeline
        
        jobs[job_id]["message"] = "Loading configuration..."
        pipeline = Idea2VideoPipeline.init_from_config(
            config_path="/app/backend/configs/idea2video.yaml"
        )
        
        jobs[job_id]["message"] = "Generating video..."
        await pipeline(idea=idea, user_requirement=user_requirement, style=style)
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Video generated successfully!"
        jobs[job_id]["working_dir"] = str(pipeline.working_dir) if hasattr(pipeline, 'working_dir') else None
        logger.info(f"Job {job_id}: Completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id}: Error - {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = f"Error: {str(e)}"

async def run_script2video(job_id: str, script: str, user_requirement: str, style: str):
    """Run script2video pipeline in background"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["message"] = "Initializing pipeline..."
        logger.info(f"Job {job_id}: Starting script2video pipeline")
        
        from backend.pipelines.script2video_pipeline import Script2VideoPipeline
        
        jobs[job_id]["message"] = "Loading configuration..."
        pipeline = Script2VideoPipeline.init_from_config(
            config_path="/app/backend/configs/script2video.yaml"
        )
        
        jobs[job_id]["message"] = "Generating video..."
        await pipeline(script=script, user_requirement=user_requirement, style=style)
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Video generated successfully!"
        jobs[job_id]["working_dir"] = str(pipeline.working_dir) if hasattr(pipeline, 'working_dir') else None
        logger.info(f"Job {job_id}: Completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id}: Error - {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = f"Error: {str(e)}"

@app.post("/api/generate/idea")
async def generate_from_idea(request: IdeaRequest, background_tasks: BackgroundTasks):
    """Generate video from idea"""
    job_id = f"idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    jobs[job_id] = {
        "status": "queued",
        "message": "Job queued",
        "created_at": datetime.now().isoformat(),
        "type": "idea2video"
    }
    
    # Run in background
    background_tasks.add_task(
        run_idea2video,
        job_id,
        request.idea,
        request.user_requirement,
        request.style
    )
    
    logger.info(f"Created job {job_id} for idea2video")
    
    return JobResponse(
        job_id=job_id,
        status="queued",
        message="Video generation started. Check job status for progress.",
        created_at=jobs[job_id]["created_at"]
    )

@app.post("/api/generate/script")
async def generate_from_script(request: ScriptRequest, background_tasks: BackgroundTasks):
    """Generate video from script"""
    job_id = f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    jobs[job_id] = {
        "status": "queued",
        "message": "Job queued",
        "created_at": datetime.now().isoformat(),
        "type": "script2video"
    }
    
    # Run in background
    background_tasks.add_task(
        run_script2video,
        job_id,
        request.script,
        request.user_requirement,
        request.style
    )
    
    logger.info(f"Created job {job_id} for script2video")
    
    return JobResponse(
        job_id=job_id,
        status="queued",
        message="Video generation started. Check job status for progress.",
        created_at=jobs[job_id]["created_at"]
    )

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get status of a specific job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return JobResponse(
        job_id=job_id,
        status=job["status"],
        message=job["message"],
        created_at=job["created_at"],
        working_dir=job.get("working_dir")
    )

@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "jobs": [
            {
                "job_id": job_id,
                **job_data
            }
            for job_id, job_data in jobs.items()
        ]
    }

@app.get("/api/videos")
async def list_videos():
    """List all generated videos"""
    videos = []
    
    # Check idea2video working directory
    idea_dir = Path("/app/backend/.working_dir/idea2video")
    if idea_dir.exists():
        for video_file in idea_dir.rglob("*.mp4"):
            try:
                stat = video_file.stat()
                videos.append(VideoInfo(
                    filename=video_file.name,
                    path=str(video_file),
                    size=stat.st_size,
                    created_at=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    type="idea2video"
                ))
            except Exception as e:
                logger.warning(f"Error reading video file {video_file}: {e}")
    
    # Check script2video working directory
    script_dir = Path("/app/backend/.working_dir/script2video")
    if script_dir.exists():
        for video_file in script_dir.rglob("*.mp4"):
            try:
                stat = video_file.stat()
                videos.append(VideoInfo(
                    filename=video_file.name,
                    path=str(video_file),
                    size=stat.st_size,
                    created_at=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    type="script2video"
                ))
            except Exception as e:
                logger.warning(f"Error reading video file {video_file}: {e}")
    
    # Sort by creation date (newest first)
    videos.sort(key=lambda x: x.created_at, reverse=True)
    
    return {"videos": videos}

@app.get("/api/videos/download/{video_type}/{filename}")
async def download_video(video_type: str, filename: str):
    """Download a specific video file"""
    if video_type not in ["idea2video", "script2video"]:
        raise HTTPException(status_code=400, detail="Invalid video type")
    
    video_path = Path(f"/app/backend/.working_dir/{video_type}") / filename
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        path=str(video_path),
        filename=filename,
        media_type="video/mp4"
    )

# Root endpoint - API info
@app.get("/")
async def root():
    """API root - returns API information"""
    return {
        "name": "ViMax API",
        "version": "1.0.0",
        "description": "AI-Powered Video Generation Platform",
        "endpoints": {
            "health": "/api/health",
            "status": "/api/status",
            "generate_idea": "/api/generate/idea",
            "generate_script": "/api/generate/script",
            "jobs": "/api/jobs",
            "job_status": "/api/jobs/{job_id}",
            "videos": "/api/videos",
            "download": "/api/videos/download/{video_type}/{filename}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
