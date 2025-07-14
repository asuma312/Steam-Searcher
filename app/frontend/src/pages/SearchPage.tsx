import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Gamepad2 } from 'lucide-react';

const SearchPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [genres, setGenres] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [priceStart, setPriceStart] = useState('');
  const [priceEnd, setPriceEnd] = useState('');
  const [filtersLoading, setFiltersLoading] = useState(true); // Novo estado para o loading dos filtros
  const navigate = useNavigate();
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    const fetchFilters = async () => {
      setFiltersLoading(true); // Inicia o loading
      try {
        const [genresRes, categoriesRes] = await Promise.all([
          fetch(`${backendUrl}/api/get_genres`),
          fetch(`${backendUrl}/api/get_categories`),
        ]);
        const genresData = await genresRes.json();
        const categoriesData = await categoriesRes.json();
        // Ordena e remove duplicatas ou valores vazios por segurança
        setGenres([...new Set(genresData.filter(Boolean))].sort());
        setCategories([...new Set(categoriesData.filter(Boolean))].sort());
      } catch (error) {
        console.error("Failed to fetch filters:", error);
      } finally {
        setFiltersLoading(false); // Finaliza o loading, mesmo se der erro
      }
    };
    fetchFilters();
  }, [backendUrl]);

  const handleGenreChange = (genre: string) => {
    setSelectedGenres(prev =>
      prev.includes(genre) ? prev.filter(g => g !== genre) : [...prev, genre]
    );
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategories(prev =>
      prev.includes(category) ? prev.filter(c => c !== category) : [...prev, category]
    );
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim() || selectedGenres.length > 0 || selectedCategories.length > 0 || priceStart || priceEnd) {
      const params = new URLSearchParams();
      if (searchQuery.trim()) {
        params.set('q', searchQuery.trim());
      }
      if (selectedGenres.length > 0) {
        params.set('genre', selectedGenres.join(','));
      }
      if (selectedCategories.length > 0) {
        params.set('category', selectedCategories.join(','));
      }
      if (priceStart) {
        params.set('price_start', priceStart);
      }
      if (priceEnd) {
        params.set('price_end', priceEnd);
      }
      navigate(`/results?${params.toString()}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center px-4 py-12">
      <div className="max-w-2xl w-full text-center">
        {/* Logo Section */}
        <div className="mb-8">
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

          {/* Filtros sempre visíveis */}
          <div className="bg-gray-800/60 p-6 rounded-lg backdrop-blur-sm text-left">
            <h3 className="text-lg font-semibold text-white mb-4 text-center border-b border-gray-700 pb-3">Filters</h3>

            {filtersLoading ? (
              <div className="text-center py-10">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto mb-3"></div>
                <p className="text-gray-400">Loading filters...</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Filtro de Preço */}
                <div>
                  <h4 className="font-semibold text-white mb-2">Price Range</h4>
                  <div className="flex items-center space-x-2">
                    <input type="number" placeholder="Min" value={priceStart} onChange={e => setPriceStart(e.target.value)} className="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500" />
                    <span className="text-gray-400">-</span>
                    <input type="number" placeholder="Max" value={priceEnd} onChange={e => setPriceEnd(e.target.value)} className="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-white placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500" />
                  </div>
                </div>

                {/* Filtro de Gênero */}
                <div>
                  <h4 className="font-semibold text-white mb-2">Genres</h4>
                  <div className="max-h-40 overflow-y-auto grid grid-cols-2 md:grid-cols-3 gap-2 p-3 bg-gray-900/50 rounded-md border border-gray-700">
                    {genres.map(genre => (
                      <label key={genre} className="flex items-center space-x-2 text-gray-300 hover:text-white cursor-pointer">
                        <input type="checkbox" checked={selectedGenres.includes(genre)} onChange={() => handleGenreChange(genre)} className="form-checkbox bg-gray-600 border-gray-500 text-blue-500 focus:ring-blue-500 rounded" />
                        <span className="truncate" title={genre}>{genre}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Filtro de Categoria */}
                <div>
                  <h4 className="font-semibold text-white mb-2">Categories</h4>
                  <div className="max-h-40 overflow-y-auto grid grid-cols-2 md:grid-cols-3 gap-2 p-3 bg-gray-900/50 rounded-md border border-gray-700">
                    {categories.map(category => (
                      <label key={category} className="flex items-center space-x-2 text-gray-300 hover:text-white cursor-pointer">
                        <input type="checkbox" checked={selectedCategories.includes(category)} onChange={() => handleCategoryChange(category)} className="form-checkbox bg-gray-600 border-gray-500 text-blue-500 focus:ring-blue-500 rounded" />
                        <span className="truncate" title={category}>{category}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          <button
            type="submit"
            className="w-full py-4 px-8 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white font-semibold rounded-xl transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-xl"
          >
            Search Games
          </button>
        </form>
      </div>
    </div>
  );
};

export default SearchPage;