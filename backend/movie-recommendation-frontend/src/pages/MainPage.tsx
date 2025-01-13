import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const MainPage: React.FC = () => {
  const [genre, setGenre] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    navigate(`/movies?genre=${genre}`);
  };

  return (
    <div>
      <h1>Movie Recommendation System</h1>
      <input
        type="text"
        value={genre}
        onChange={(e) => setGenre(e.target.value)}
        placeholder="Enter a genre (e.g., Action)"
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default MainPage;
