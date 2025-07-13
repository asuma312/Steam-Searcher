import React from 'react';
import { useState } from 'react';
import { ExternalLink, DollarSign, Monitor, Apple, Smartphone, Tag, Grid3X3 } from 'lucide-react';
import { GameData } from '../types/Game';

interface GameCardProps {
  game: GameData;
}

const GameCard: React.FC<GameCardProps> = ({ game }) => {
  const [showDetails, setShowDetails] = useState(false);

  const formatPrice = (price: number) => {
    return price === 0 ? 'Free' : `$${price.toFixed(2)}`;
  };

  const formatRequirements = (requirements: Record<string, string>) => {
    return Object.entries(requirements).map(([key, value]) => (
      <div key={key} className="flex justify-between py-1 border-b border-gray-600 last:border-b-0">
        <span className="text-gray-300 capitalize font-medium">{key.replace('_', ' ')}:</span>
        <span className="text-white text-right ml-2">{value}</span>
      </div>
    ));
  };

  const hasRequirements = (requirements: Record<string, string>) => {
    return Object.keys(requirements).length > 0;
  };

  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] border border-gray-700 hover:border-gray-600 relative cursor-pointer"
         onClick={() => setShowDetails(!showDetails)}>
      {/* Game Image */}
      <div className="relative h-48 overflow-hidden bg-gray-700">
        <img
          src={game.image}
          alt={game.name}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = 'https://images.pexels.com/photos/735911/pexels-photo-735911.jpeg?auto=compress&cs=tinysrgb&w=400&h=225';
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
      </div>

      {/* Card Content */}
      <div className="p-6">
        {/* Title and Price Row */}
        <div className="flex items-start justify-between mb-3">
          <a
            href={game.link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center group"
          >
            <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors duration-200 mr-2 line-clamp-2">
              {game.name}
            </h3>
            <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-400 transition-colors duration-200 flex-shrink-0" />
          </a>

          <div className="flex items-center bg-green-600 text-white px-3 py-1 rounded-full text-sm font-semibold ml-4 flex-shrink-0">
            <DollarSign className="w-3 h-3 mr-1" />
            {formatPrice(game.price)}
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-300 text-sm leading-relaxed line-clamp-3">
          {game.description}
        </p>

        {/* System Requirements Icons */}
        <div className="flex items-center space-x-3 mb-3">
          <span className="text-gray-400 text-sm font-medium">System Requirements:</span>
          <div className="flex space-x-2">
            {hasRequirements(game.pc_requirements) && (
              <div className="flex items-center text-gray-300 hover:text-blue-400 transition-colors">
                <Monitor className="w-4 h-4" />
                <span className="text-xs ml-1">PC</span>
              </div>
            )}
            {hasRequirements(game.mac_requirements) && (
              <div className="flex items-center text-gray-300 hover:text-blue-400 transition-colors">
                <Apple className="w-4 h-4" />
                <span className="text-xs ml-1">Mac</span>
              </div>
            )}
            {hasRequirements(game.linux_requirements) && (
              <div className="flex items-center text-gray-300 hover:text-blue-400 transition-colors">
                <Smartphone className="w-4 h-4" />
                <span className="text-xs ml-1">Linux</span>
              </div>
            )}
          </div>
        </div>

        {/* Genres */}
        {game.genres && game.genres.length > 0 && (
          <div className="mb-3">
            <div className="flex items-center mb-2">
              <Tag className="w-4 h-4 text-gray-400 mr-2" />
              <span className="text-gray-400 text-sm font-medium">Gêneros:</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {game.genres.slice(0, 4).map((genre) => (
                <span
                  className="px-2 py-1 bg-blue-600/20 text-blue-300 text-xs rounded-full border border-blue-600/30"
                >
    {genre.replace(/^\d+\s*/, '').replace(/"/g, '')}
                </span>
              ))}
              {game.genres.length > 4 && (
                <span className="px-2 py-1 bg-gray-600/20 text-gray-300 text-xs rounded-full border border-gray-600/30">
                  +{game.genres.length - 4} mais
                </span>
              )}
            </div>
          </div>
        )}

        {/* Categories */}
        {game.categories && game.categories.length > 0 && (
          <div className="mb-4">
            <div className="flex items-center mb-2">
              <Grid3X3 className="w-4 h-4 text-gray-400 mr-2" />
              <span className="text-gray-400 text-sm font-medium">Categorias:</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {game.categories.slice(0, 3).map((category) => (
                <span
                  className="px-2 py-1 bg-green-600/20 text-green-300 text-xs rounded-full border border-green-600/30"
                >
    {category.replace(/^\d+\s*/, '').replace(/"/g, '')}
                </span>
              ))}
              {game.categories.length > 3 && (
                <span className="px-2 py-1 bg-gray-600/20 text-gray-300 text-xs rounded-full border border-gray-600/30">
                  +{game.categories.length - 3} mais
                </span>
              )}
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="pt-4 border-t border-gray-700">
          <a
            href={game.link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200"
          >
            View on Steam
            <ExternalLink className="w-4 h-4 ml-2" />
          </a>
        </div>
      </div>

      {/* System Requirements Hover Overlay */}
      {showDetails && (
        <div className="absolute inset-0 bg-gray-900/95 backdrop-blur-sm transition-all duration-300 overflow-y-auto z-20">
        <div className="p-6 min-h-full flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xl font-bold text-white flex items-center">
              <Monitor className="w-5 h-5 mr-2 text-blue-400" />
              System Requirements
            </h4>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowDetails(false);
              }}
              className="text-gray-400 hover:text-white transition-colors text-xl font-bold"
            >
              ×
            </button>
          </div>

          <div className="space-y-6 flex-1">
            {/* PC Requirements */}
            {hasRequirements(game.pc_requirements) && (
              <div>
                <h5 className="text-lg font-semibold text-blue-400 mb-3 flex items-center">
                  <Monitor className="w-4 h-4 mr-2" />
                  PC (Windows)
                </h5>
                <div className="bg-gray-800/50 rounded-lg p-4 space-y-2">
                  {formatRequirements(game.pc_requirements)}
                </div>
              </div>
            )}

            {/* Mac Requirements */}
            {hasRequirements(game.mac_requirements) && (
              <div>
                <h5 className="text-lg font-semibold text-blue-400 mb-3 flex items-center">
                  <Apple className="w-4 h-4 mr-2" />
                  Mac (macOS)
                </h5>
                <div className="bg-gray-800/50 rounded-lg p-4 space-y-2">
                  {formatRequirements(game.mac_requirements)}
                </div>
              </div>
            )}

            {/* Linux Requirements */}
            {hasRequirements(game.linux_requirements) && (
              <div>
                <h5 className="text-lg font-semibold text-blue-400 mb-3 flex items-center">
                  <Smartphone className="w-4 h-4 mr-2" />
                  Linux
                </h5>
                <div className="bg-gray-800/50 rounded-lg p-4 space-y-2">
                  {formatRequirements(game.linux_requirements)}
                </div>
              </div>
            )}
          </div>

          {/* Genres Section */}
          {game.genres && game.genres.length > 0 && (
            <div className="mt-6">
              <h5 className="text-lg font-semibold text-blue-400 mb-3 flex items-center">
                <Tag className="w-4 h-4 mr-2" />
                Gêneros
              </h5>
              <div className="bg-gray-800/50 rounded-lg p-4">
                <div className="flex flex-wrap gap-2">
                  {game.genres.map((genre) => (
                    <span
                      className="px-3 py-1 bg-blue-600/30 text-blue-200 text-sm rounded-full border border-blue-600/50"
                    >
    {genre.replace(/^\d+\s*/, '').replace(/"/g, '')}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Categories Section */}
          {game.categories && game.categories.length > 0 && (
            <div className="mt-6">
              <h5 className="text-lg font-semibold text-blue-400 mb-3 flex items-center">
                <Grid3X3 className="w-4 h-4 mr-2" />
                Categorias
              </h5>
              <div className="bg-gray-800/50 rounded-lg p-4">
                <div className="flex flex-wrap gap-2">
                  {game.categories.map((category) => (
                    <span
                      className="px-3 py-1 bg-green-600/30 text-green-200 text-sm rounded-full border border-green-600/50"
                    >
    {category.replace(/^\d+\s*/, '').replace(/"/g, '')}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Steam Button Inside Overlay */}
          <div className="mt-6 pt-4 border-t border-gray-700">
            <a
              href={game.link}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="inline-flex items-center justify-center w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200"
            >
              View on Steam
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
            <p className="text-gray-400 text-xs text-center mt-2">
              Clique no X ou fora da área para fechar
            </p>
          </div>
        </div>
        </div>
      )}
    </div>
  );
};

export default GameCard;