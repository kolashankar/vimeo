import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const JobProgress = ({ jobId }) => {
  const [jobStatus, setJobStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!jobId) return;

    const pollJobStatus = async () => {
      try {
        const status = await apiService.getJobStatus(jobId);
        setJobStatus(status);
        
        // Stop polling if job is completed or failed
        if (status.status === 'completed' || status.status === 'failed') {
          setLoading(false);
        }
      } catch (error) {
        console.error('Failed to fetch job status:', error);
        setLoading(false);
      }
    };

    // Initial fetch
    pollJobStatus();

    // Poll every 5 seconds
    const interval = setInterval(pollJobStatus, 5000);

    return () => clearInterval(interval);
  }, [jobId]);

  if (!jobStatus) {
    return (
      <div className="mt-6 p-4 bg-blue-50 rounded-lg" data-testid="job-progress">
        <div className="flex items-center">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500 mr-3"></div>
          <span className="text-blue-700">Loading job status...</span>
        </div>
      </div>
    );
  }

  const getStatusColor = () => {
    switch (jobStatus.status) {
      case 'completed':
        return 'bg-green-50 border-green-400';
      case 'failed':
        return 'bg-red-50 border-red-400';
      case 'processing':
        return 'bg-blue-50 border-blue-400';
      default:
        return 'bg-gray-50 border-gray-400';
    }
  };

  const getStatusIcon = () => {
    switch (jobStatus.status) {
      case 'completed':
        return '✅';
      case 'failed':
        return '❌';
      case 'processing':
        return '⏳';
      default:
        return '🕒';
    }
  };

  return (
    <div className={`mt-6 p-4 border-l-4 rounded-lg ${getStatusColor()}`} data-testid="job-progress">
      <div className="flex items-start">
        <div className="text-2xl mr-3">{getStatusIcon()}</div>
        <div className="flex-1">
          <div className="font-semibold text-gray-800 mb-1">
            Job: {jobId}
          </div>
          <div className="text-sm text-gray-700 mb-2">
            Status: <span className="font-medium capitalize">{jobStatus.status}</span>
          </div>
          <div className="text-sm text-gray-600">
            {jobStatus.message}
          </div>
          {jobStatus.working_dir && (
            <div className="mt-2 text-xs text-gray-500">
              Working Directory: {jobStatus.working_dir}
            </div>
          )}
          {jobStatus.status === 'processing' && (
            <div className="mt-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full animate-pulse" style={{ width: '70%' }}></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">This may take several minutes...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobProgress;
