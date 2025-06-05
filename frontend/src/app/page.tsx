'use client';

import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [clonedHtml, setClonedHtml] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:8001/api/clone', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to clone website');
      }
      
      const data = await response.json();
      setClonedHtml(data.html);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Decorative orchid elements */}
      <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-pink-500/20 to-transparent" />
      <div className="absolute bottom-0 right-0 w-64 h-64 bg-gradient-to-t from-pink-500/20 to-transparent rounded-full blur-3xl" />
      
      <main className="relative min-h-screen p-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-pink-600 bg-clip-text text-transparent">
              Orchids Website Cloner
            </h1>
            <p className="text-gray-400">
              Transform any website into a beautiful clone with AI
            </p>
          </div>
          
          {/* Input Form */}
          <div className="bg-black/50 backdrop-blur-sm border border-pink-500/20 rounded-xl p-6 mb-8 shadow-lg">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="flex gap-4">
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Enter website URL"
                  className="flex-1 p-3 bg-black/50 border border-pink-500/30 rounded-lg focus:outline-none focus:border-pink-500 text-white placeholder-gray-500"
                  required
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-600 text-white rounded-lg hover:from-pink-600 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium shadow-lg shadow-pink-500/20"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Cloning...
                    </span>
                  ) : (
                    'Clone Website'
                  )}
                </button>
              </div>
            </form>
          </div>

          {error && (
            <div className="mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400">
              {error}
            </div>
          )}

          {clonedHtml && (
            <div className="bg-black/50 backdrop-blur-sm border border-pink-500/20 rounded-xl p-6 shadow-lg">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-pink-400">Preview</h2>
                <div className="text-sm text-gray-400">Powered by Claude AI</div>
              </div>
              <div className="border border-pink-500/20 rounded-lg overflow-hidden bg-white">
                <iframe
                  srcDoc={clonedHtml}
                  className="w-full h-[600px]"
                  sandbox="allow-same-origin"
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
