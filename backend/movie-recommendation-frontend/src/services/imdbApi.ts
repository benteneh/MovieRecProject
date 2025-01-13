import axios from 'axios';
import { Movie } from '../types/movie';

interface MoviesResponse {
  movies: Movie[];
}

const API_URL = 'http://127.0.0.1:5000'; 

export const fetchMoviesByGenre = async (genre: string): Promise<Movie[]> => {
  try {
    const response = await axios.get<MoviesResponse>(`${API_URL}/movies`, {
      params: { genre },
    });
    return response.data.movies;
  } catch (error) {
    console.error('Error fetching movies by genre:', error);
    throw error;
  }
};
