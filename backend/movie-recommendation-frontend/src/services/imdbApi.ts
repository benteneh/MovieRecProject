import axios from 'axios';
import { Movie } from '../types/movie';

interface MoviesResponse {
  movies: Movie[];
  total: number;
  page: number;
  pages: number;
}

const API_URL = 'http://127.0.0.1:5000'; 

/**
 * Fetch movies by genre with pagination.
 * 
 * @param genre - Genre to filter movies by.
 * @param page - Current page number (default: 1).
 * @param perPage - Number of movies per page (default: 10).
 * @returns - MoviesResponse containing movies and pagination details.
 */
export const fetchMoviesByGenre = async (
  genre: string,
  page: number = 1,
  perPage: number = 10
): Promise<MoviesResponse> => {
  try {
    const response = await axios.get<MoviesResponse>(`${API_URL}/movies`, {
      params: { genre, page, per_page: perPage },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching movies by genre:', error);
    throw error;
  }
};
