import React, { useState } from 'react';
import { apiService } from '../services/api';
import JobProgress from './JobProgress';

const IdeaToVideo = () => {
  const [formData, setFormData] = useState({
    idea: '',
    user_requirement: 'For adults, do not exceed 3 scenes.',
    style: 'Realistic',
  });
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    setJobId(null);

    try {
      const response = await apiService.generateFromIdea(formData);
      setJobId(response.job_id);
      setSuccess('Video generation started! Check progress below.');
      // Reset form
      setFormData({
        idea: '',
        user_requirement: 'For adults, do not exceed 3 scenes.',
        style: 'Realistic',
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start video generation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" data-testid="idea-to-video-form">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          💡 Idea to Video
        </h2>
        <p className="text-gray-600">
          Describe your idea and let AI transform it into a complete video story.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="idea" className="block text-sm font-semibold text-gray-700 mb-2">
            Your Idea *
          </label>
          <textarea
            id="idea"
            data-testid="idea-input"
            value={formData.idea}
            onChange={(e) => setFormData({ ...formData, idea: e.target.value })}
            className="input-field min-h-[150px] resize-y"
            placeholder="Describe your video idea... (e.g., A cat and dog become best friends and go on an adventure)"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="requirement" className="block text-sm font-semibold text-gray-700 mb-2">
              Requirements
            </label>
            <input
              type="text"
              id="requirement"
              data-testid="requirement-input"
              value={formData.user_requirement}
              onChange={(e) => setFormData({ ...formData, user_requirement: e.target.value })}
              className="input-field"
              placeholder="E.g., For adults, do not exceed 3 scenes"
            />
          </div>

          <div>
            <label htmlFor="style" className="block text-sm font-semibold text-gray-700 mb-2">
              Style
            </label>
            <input
              type="text"
              id="style"
              data-testid="style-input"
              value={formData.style}
              onChange={(e) => setFormData({ ...formData, style: e.target.value })}
              className="input-field"
              placeholder="E.g., Realistic, Cartoon, Anime"
            />
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border-l-4 border-red-400 rounded" data-testid="error-message">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {success && (
          <div className="p-4 bg-green-50 border-l-4 border-green-400 rounded" data-testid="success-message">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-green-700">{success}</p>
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !formData.idea}
          className="btn-primary w-full"
          data-testid="submit-button"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Starting Generation...
            </span>
          ) : (
            '🎥 Generate Video from Idea'
          )}
        </button>
      </form>

      {jobId && <JobProgress jobId={jobId} />}
    </div>
  );
};

export default IdeaToVideo;
