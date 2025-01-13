import React, { useEffect, useState } from 'react';
import { fetchMoviesByGenre } from '../services/imdbApi';
import { Movie } from '../types/movie';

const MoviesPage: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadMovies = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const genre = urlParams.get('genre') || 'all';

      try {
        const data = await fetchMoviesByGenre(genre);
        console.log('Movies fetched:', data);
        setMovies(data);
      } catch (err) {
        setError('Failed to fetch movies. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadMovies();
  }, []);

  if (loading) return <div>Loading movies...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="movie-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
      {movies.map((movie) => (
        <div
          key={movie.Title}
          className="movie-card bg-gray-800 rounded-lg shadow-lg p-4 text-white hover:scale-105 transition-transform"
        >
          <img
            className="rounded-t-lg w-full h-64 object-cover"
            src={movie.Poster || 'default-poster.jpg'}
            alt={movie.Title || 'Untitled'}
          />
          <div className="p-4">
            <h2 className="text-lg font-bold mb-2">{movie.Title || 'Untitled'}</h2>
            <p className="text-sm mb-2">Rating: {movie.imdbRating || 'N/A'}</p>
            <p className="text-xs text-gray-400">{movie.Plot || 'No description available.'}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MoviesPage;
