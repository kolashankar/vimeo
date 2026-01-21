import React from 'react';

const StatusCard = ({ status, loading }) => {
  if (loading) {
    return (
      <div className="card mb-6" data-testid="status-card">
        <h2 className="text-xl font-bold mb-4 text-gray-800">📊 System Status</h2>
        <div className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
        </div>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="card mb-6" data-testid="status-card">
        <h2 className="text-xl font-bold mb-4 text-gray-800">📊 System Status</h2>
        <div className="text-center py-4 text-gray-500">
          Unable to fetch system status
        </div>
      </div>
    );
  }

  return (
    <div className="card mb-6" data-testid="status-card">
      <h2 className="text-xl font-bold mb-4 text-gray-800">📊 System Status</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          className={`p-4 rounded-lg text-center ${
            status.chat_available ? 'bg-green-50' : 'bg-red-50'
          }`}
          data-testid="status-chat"
        >
          <div className="text-3xl mb-2">
            {status.chat_available ? '✅' : '❌'}
          </div>
          <div className="font-semibold text-gray-800">Chat Model</div>
          <div className="text-sm text-gray-600">
            {status.chat_available ? 'Available' : 'Unavailable'}
          </div>
        </div>

        <div
          className={`p-4 rounded-lg text-center ${
            status.image_available ? 'bg-green-50' : 'bg-yellow-50'
          }`}
          data-testid="status-image"
        >
          <div className="text-3xl mb-2">
            {status.image_available ? '✅' : '⚠️'}
          </div>
          <div className="font-semibold text-gray-800">Image Generation</div>
          <div className="text-sm text-gray-600">
            {status.image_available ? 'Available' : 'Quota Limited'}
          </div>
        </div>

        <div
          className="p-4 rounded-lg text-center bg-blue-50"
          data-testid="status-video"
        >
          <div className="text-3xl mb-2">⏳</div>
          <div className="font-semibold text-gray-800">Video Generation</div>
          <div className="text-sm text-gray-600">Ready</div>
        </div>
      </div>

      {!status.image_available && (
        <div className="mt-4 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded" data-testid="quota-warning">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                <strong>Image Generation Quota Exhausted:</strong> Enable billing at{' '}
                <a
                  href="https://aistudio.google.com/app/billing"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline font-semibold"
                >
                  Google AI Studio
                </a>
                {' '}or wait ~24 hours for reset.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatusCard;
