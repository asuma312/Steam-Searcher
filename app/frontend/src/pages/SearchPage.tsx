import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Gamepad2 } from 'lucide-react';

const SearchPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/results?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center">
        {/* Logo Section */}
        <div className="mb-12">
          <div className="flex items-center justify-center mb-6">
            <Gamepad2 className="w-16 h-16 text-blue-400 mr-4" />
            <h1 className="text-6xl font-bold text-white">
              Steam<span className="text-blue-400">Searcher</span>
            </h1>
          </div>
          <p className="text-xl text-gray-300 font-light">
            Discover your next favorite game
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="space-y-6">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none">
              <Search className="h-6 w-6 text-gray-400" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search for games..."
              className="w-full pl-16 pr-6 py-4 bg-gray-800 border-2 border-gray-700 rounded-xl text-white text-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 hover:border-gray-600"
            />
          </div>
          
          <button
            type="submit"
            disabled={!searchQuery.trim()}
            className="w-full py-4 px-8 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 disabled:from-gray-700 disabled:to-gray-600 text-white font-semibold rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:scale-100 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
          >
            Search Games
          </button>
        </form>

        {/* Features */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-gray-300">
          <div className="bg-gray-800/50 p-6 rounded-lg backdrop-blur-sm">
            <h3 className="font-semibold text-white mb-2">Fast Search</h3>
            <p className="text-sm">Lightning-fast game discovery powered by Steam's database</p>
          </div>
          <div className="bg-gray-800/50 p-6 rounded-lg backdrop-blur-sm">
            <h3 className="font-semibold text-white mb-2">Real Prices</h3>
            <p className="text-sm">Up-to-date pricing information directly from Steam</p>
          </div>
          <div className="bg-gray-800/50 p-6 rounded-lg backdrop-blur-sm">
            <h3 className="font-semibold text-white mb-2">Detailed Info</h3>
            <p className="text-sm">Comprehensive game descriptions and details</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;