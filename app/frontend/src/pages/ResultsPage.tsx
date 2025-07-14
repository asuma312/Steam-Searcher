import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { ArrowLeft, Search } from 'lucide-react';
import GameCard from '../components/GameCard';
import { GameData } from '../types/Game';

const ResultsPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [games, setGames] = useState<GameData[]>([]);
  const [loading, setLoading] = useState(true);

  // Extract all parameters from the URL
  const query = searchParams.get('q') || '';
  const genres = searchParams.get('genre')?.split(',') || [];
  const categories = searchParams.get('category')?.split(',') || [];
  const price_start = searchParams.get('price_start');
  const price_end = searchParams.get('price_end');

  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    const fetchGames = async () => {
      setLoading(true);

      const searchBody: {
        query: string;
        genre: string[];
        category: string[];
        price_start?: number;
        price_end?: number;
      } = {
        query: query,
        genre: genres.filter(Boolean), // Remove empty strings
        category: categories.filter(Boolean), // Remove empty strings
      };

      if (price_start) {
        searchBody.price_start = parseFloat(price_start);
      }
      if (price_end) {
        searchBody.price_end = parseFloat(price_end);
      }

      const response = await fetch(
          `${backendUrl}/api/search`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchBody),
          }
      );

      const fetchedGamesData = await response.json();
      setGames(fetchedGamesData);
      setLoading(false);
    }
    fetchGames();
  }, [searchParams, backendUrl]); // Depend on searchParams to refetch when URL changes

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-white text-xl">Searching for games...</p>
        </div>
      </div>
    );
  }

  const displayQuery = query || [...genres, ...categories].join(', ') || 'All Games';

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link
                to="/"
                className="flex items-center text-gray-300 hover:text-white transition-colors duration-200"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Search
              </Link>
              <div className="text-gray-400">|</div>
              <h1 className="text-xl font-semibold text-white">SteamSearcher</h1>
            </div>

            <div className="flex items-center space-x-2 text-gray-300">
              <Search className="w-5 h-5" />
              <span className="font-medium truncate" title={displayQuery}>"{displayQuery}"</span>
              <span className="text-gray-500">({games.length} results)</span>
            </div>
          </div>
        </div>
      </header>

      {/* Results Grid */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {games.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-400 text-xl">No games found for your criteria</p>
            <Link
              to="/"
              className="inline-block mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
            >
              Try Another Search
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {games.map((game) => (
              <GameCard key={game.id} game={game} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default ResultsPage;