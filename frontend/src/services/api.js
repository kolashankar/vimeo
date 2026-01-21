import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for video generation
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/api/health');
    return response.data;
  },

  // System status
  async getStatus() {
    const response = await api.get('/api/status');
    return response.data;
  },

  // Generate video from idea
  async generateFromIdea(data) {
    const response = await api.post('/api/generate/idea', data);
    return response.data;
  },

  // Generate video from script
  async generateFromScript(data) {
    const response = await api.post('/api/generate/script', data);
    return response.data;
  },

  // Get job status
  async getJobStatus(jobId) {
    const response = await api.get(`/api/jobs/${jobId}`);
    return response.data;
  },

  // List all jobs
  async listJobs() {
    const response = await api.get('/api/jobs');
    return response.data;
  },

  // List all videos
  async listVideos() {
    const response = await api.get('/api/videos');
    return response.data;
  },

  // Get video download URL
  getVideoDownloadUrl(videoType, filename) {
    return `${API_URL}/api/videos/download/${videoType}/${filename}`;
  },
};

export default apiService;
