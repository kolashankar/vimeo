import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const VideoGallery = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      setLoading(true);
      const response = await apiService.listVideos();
      setVideos(response.videos || []);
    } catch (err) {
      setError('Failed to load videos');
      console.error('Error fetching videos:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  if (loading) {
    return (
      <div className="card" data-testid="video-gallery">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          🎬 Video Gallery
        </h2>
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card" data-testid="video-gallery">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          🎬 Video Gallery
        </h2>
        <div className="text-center py-12 text-red-600">{error}</div>
      </div>
    );
  }

  if (videos.length === 0) {
    return (
      <div className="card" data-testid="video-gallery">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          🎬 Video Gallery
        </h2>
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🎥</div>
          <p className="text-gray-600 text-lg">No videos generated yet</p>
          <p className="text-gray-500 text-sm mt-2">
            Start by creating a video from an idea or script!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card" data-testid="video-gallery">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          🎬 Video Gallery
        </h2>
        <button
          onClick={fetchVideos}
          className="text-primary-600 hover:text-primary-700 font-medium text-sm"
          data-testid="refresh-button"
        >
          🔄 Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {videos.map((video, index) => (
          <div
            key={index}
            className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
            data-testid="video-card"
          >
            <div className="aspect-video bg-gray-100 flex items-center justify-center">
              <div className="text-6xl">🎬</div>
            </div>
            <div className="p-4">
              <h3 className="font-semibold text-gray-800 mb-2 truncate" title={video.filename}>
                {video.filename}
              </h3>
              <div className="space-y-1 text-sm text-gray-600">
                <div className="flex items-center">
                  <span className="w-16">Type:</span>
                  <span className="status-badge bg-blue-100 text-blue-800">
                    {video.type}
                  </span>
                </div>
                <div className="flex items-center">
                  <span className="w-16">Size:</span>
                  <span>{formatFileSize(video.size)}</span>
                </div>
                <div className="flex items-center">
                  <span className="w-16">Created:</span>
                  <span className="text-xs">{formatDate(video.created_at)}</span>
                </div>
              </div>
              <div className="mt-4">
                <a
                  href={apiService.getVideoDownloadUrl(video.type, video.filename)}
                  download
                  className="block w-full text-center bg-primary-500 text-white py-2 rounded-lg hover:bg-primary-600 transition-colors"
                  data-testid="download-button"
                >
                  ⬇️ Download
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VideoGallery;
