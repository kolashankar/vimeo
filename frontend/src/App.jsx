import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatusCard from './components/StatusCard';
import IdeaToVideo from './components/IdeaToVideo';
import ScriptToVideo from './components/ScriptToVideo';
import VideoGallery from './components/VideoGallery';
import Footer from './components/Footer';
import { apiService } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('idea');
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const status = await apiService.getStatus();
      setSystemStatus(status);
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pb-20">
      <Header />
      
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* System Status */}
        <StatusCard status={systemStatus} loading={loading} />

        {/* Tab Navigation */}
        <div className="card mb-6">
          <div className="flex space-x-4 border-b border-gray-200">
            <button
              onClick={() => setActiveTab('idea')}
              className={`px-6 py-3 font-semibold transition-colors duration-200 border-b-2 ${
                activeTab === 'idea'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
              data-testid="tab-idea"
            >
              💡 Idea to Video
            </button>
            <button
              onClick={() => setActiveTab('script')}
              className={`px-6 py-3 font-semibold transition-colors duration-200 border-b-2 ${
                activeTab === 'script'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
              data-testid="tab-script"
            >
              📝 Script to Video
            </button>
            <button
              onClick={() => setActiveTab('gallery')}
              className={`px-6 py-3 font-semibold transition-colors duration-200 border-b-2 ${
                activeTab === 'gallery'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
              data-testid="tab-gallery"
            >
              🎬 Video Gallery
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {activeTab === 'idea' && <IdeaToVideo />}
          {activeTab === 'script' && <ScriptToVideo />}
          {activeTab === 'gallery' && <VideoGallery />}
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default App;
