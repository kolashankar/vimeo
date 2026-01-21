# ViMax Web Interface

> 🎬 AI-Powered Video Generation Platform with Modern Web Interface

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Features

- **💡 Idea to Video**: Transform raw ideas into complete video stories
- **📝 Script to Video**: Generate videos from screenplay scripts
- **🎨 Modern UI**: Beautiful, responsive interface built with React and TailwindCSS
- **⚡ Real-time Updates**: Track video generation progress in real-time
- **🎥 Video Gallery**: Browse and download all generated videos
- **🔄 Background Processing**: Non-blocking video generation with job queuing

## 🏗️ Architecture

### Backend (`/app/backend/`)
- **Framework**: FastAPI (Python)
- **Video Generation**: Multi-agent pipeline system
- **APIs**: Google GenAI (Gemini, Veo, Nano Banana)
- **Features**: 
  - Asynchronous video generation
  - Job status tracking
  - RESTful API endpoints

### Frontend (`/app/frontend/`)
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS with custom theme
- **State Management**: React Hooks
- **API Client**: Axios
- **Features**:
  - Responsive design
  - Real-time status updates
  - Video gallery with download

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Yarn package manager
- Google AI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kolashankar/vimeo.git
cd vimeo
```

2. **Backend Setup**
```bash
cd backend

# Install Python dependencies (if using uv)
uv sync

# Or using pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Google API key
```

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
yarn install
```

4. **Start Services**

Using Supervisor (production):
```bash
sudo supervisorctl restart all
```

Or manually (development):

Terminal 1 - Backend:
```bash
cd backend
python3 -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
yarn dev
```

5. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## 📖 API Documentation

### Core Endpoints

#### System Status
```bash
GET /api/health
GET /api/status
```

#### Video Generation
```bash
POST /api/generate/idea
POST /api/generate/script
```

**Request Body (Idea to Video)**:
```json
{
  "idea": "A cat and dog become best friends...",
  "user_requirement": "For adults, do not exceed 3 scenes.",
  "style": "Realistic"
}
```

**Request Body (Script to Video)**:
```json
{
  "script": "EXT. SCHOOL GYM - DAY\n...",
  "user_requirement": "Fast-paced with no more than 15 shots.",
  "style": "Anime Style"
}
```

#### Job Management
```bash
GET /api/jobs           # List all jobs
GET /api/jobs/{job_id}  # Get job status
```

#### Video Management
```bash
GET /api/videos         # List all videos
GET /api/videos/download/{type}/{filename}  # Download video
```

## 🎨 UI Components

### Main Components
- **Header**: Application branding and navigation
- **StatusCard**: System health and API availability
- **IdeaToVideo**: Idea input form with validation
- **ScriptToVideo**: Script input form with screenplay support
- **JobProgress**: Real-time job status with progress indicator
- **VideoGallery**: Video listing with download functionality
- **Footer**: Links and version information

### Design System
- **Colors**: Purple gradient theme (Primary: #667eea, Secondary: #764ba2)
- **Typography**: Clean, modern font stack
- **Layout**: Responsive grid system
- **Animations**: Smooth transitions and loading states

## 📁 Project Structure

```
/app/
├── backend/                 # Backend application
│   ├── agents/             # AI agent modules
│   ├── pipelines/          # Video generation pipelines
│   ├── tools/              # Image/video generation tools
│   ├── interfaces/         # Data interfaces
│   ├── utils/              # Utility functions
│   ├── configs/            # Configuration files
│   ├── server.py           # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/               # Frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   ├── App.jsx         # Main application component
│   │   ├── main.jsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   └── tailwind.config.js  # Tailwind configuration
│
├── assets/                 # Documentation assets
├── implementation.md       # Development plan
└── README.md              # This file
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/configs/idea2video.yaml` or `backend/configs/script2video.yaml`:

```yaml
chat_model:
  init_args:
    model: gemini-2.5-flash-lite-preview-09-2025
    model_provider: google_genai
    api_key: YOUR_API_KEY

image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: YOUR_API_KEY

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: YOUR_API_KEY
```

### Frontend Configuration

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:8001
VITE_APP_NAME=ViMax
VITE_APP_VERSION=1.0.0
```

## 🧪 Testing

### Backend API Testing
```bash
# Health check
curl http://localhost:8001/api/health

# Status check
curl http://localhost:8001/api/status

# Generate video from idea
curl -X POST http://localhost:8001/api/generate/idea \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "A cat exploring a magical forest",
    "user_requirement": "For children, 2 scenes max",
    "style": "Cartoon"
  }'

# Check job status
curl http://localhost:8001/api/jobs/{job_id}
```

### Frontend Testing
Open http://localhost:3000 in your browser and test:
1. System status display
2. Idea to video form submission
3. Script to video form submission
4. Job progress tracking
5. Video gallery and downloads

## 📊 Performance

- **Video Generation**: 3-10 minutes depending on complexity
- **API Response**: < 100ms for status endpoints
- **Frontend Load**: < 2 seconds initial load
- **Real-time Updates**: 5-second polling interval

## 🔐 Security

- CORS configured for frontend-backend communication
- API key stored in environment variables
- No sensitive data in frontend
- Rate limiting on API endpoints (configured in YAML)

## 🐛 Troubleshooting

### Backend Issues

**Import Errors**:
```bash
export PYTHONPATH=/app/backend:/app
```

**Port Already in Use**:
```bash
sudo supervisorctl stop backend
# Or kill the process using port 8001
lsof -ti:8001 | xargs kill -9
```

**API Key Issues**:
- Verify API key in `backend/configs/*.yaml`
- Check quota at https://aistudio.google.com

### Frontend Issues

**Dependencies Not Found**:
```bash
cd frontend
rm -rf node_modules yarn.lock
yarn install
```

**Build Errors**:
```bash
cd frontend
yarn build
```

**Port Already in Use**:
```bash
sudo supervisorctl stop frontend
# Or kill the process using port 3000
lsof -ti:3000 | xargs kill -9
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original ViMax project: [HKUDS/ViMax](https://github.com/HKUDS/ViMax)
- Google AI for Gemini and Veo APIs
- FastAPI and React communities

## 📞 Support

- GitHub Issues: [Report a bug](https://github.com/kolashankar/vimeo/issues)
- Documentation: [Implementation Plan](implementation.md)

## 🔄 Version History

- **v1.0.0** (2025-01) - Initial release
  - Backend reorganization
  - Modern React frontend
  - Complete API integration
  - Video gallery
  - Real-time job tracking

---

Made with ❤️ by the ViMax Team
