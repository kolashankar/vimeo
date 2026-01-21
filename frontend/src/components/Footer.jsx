import React from 'react';

const Footer = () => {
  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-white/10 backdrop-blur-md border-t border-white/20">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col md:flex-row justify-between items-center text-white text-sm">
          <div className="mb-2 md:mb-0">
            <span className="font-semibold">ViMax</span> - AI-Powered Video Generation
          </div>
          <div className="flex space-x-6">
            <a
              href="https://github.com/HKUDS/ViMax"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white/80 transition-colors"
            >
              GitHub
            </a>
            <a
              href="https://aistudio.google.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white/80 transition-colors"
            >
              Google AI Studio
            </a>
            <span className="text-white/60">v1.0.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
