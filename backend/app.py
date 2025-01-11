from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# OMDb API details
API_KEY = "6a9cfac6"
BASE_URL = "http://www.omdbapi.com/"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.String(4))
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    actors = db.Column(db.Text)
    imdb_rating = db.Column(db.String(10))
    plot = db.Column(db.Text)
    poster = db.Column(db.Text)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Movie Recommendation System!'})

@app.route('/movie', methods=['GET'])
def get_movie_details():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Please provide a movie title'}), 400

    # Check if the movie is already in the database
    movie = Movie.query.filter_by(title=title).first()
    if movie:
        return jsonify({
            'Title': movie.title,
            'Year': movie.year,
            'Genre': movie.genre,
            'Director': movie.director,
            'Actors': movie.actors,
            'imdbRating': movie.imdb_rating,
            'Plot': movie.plot,
            'Poster': movie.poster
        })

    # Fetch from OMDb API if not found in database
    params = {'apikey': API_KEY, 't': title}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            new_movie = Movie(
                title=data.get('Title'),
                year=data.get('Year'),
                genre=data.get('Genre'),
                director=data.get('Director'),
                actors=data.get('Actors'),
                imdb_rating=data.get('imdbRating'),
                plot=data.get('Plot'),
                poster=data.get('Poster')
            )
            db.session.add(new_movie)
            db.session.commit()

            return jsonify({
                'Title': data.get('Title'),
                'Year': data.get('Year'),
                'Genre': data.get('Genre'),
                'Director': data.get('Director'),
                'Actors': data.get('Actors'),
                'imdbRating': data.get('imdbRating'),
                'Plot': data.get('Plot'),
                'Poster': data.get('Poster')
            })
        else:
            return jsonify({'error': 'Movie not found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch data from OMDb'}), 500

@app.route('/movies-by-genre', methods=['GET'])
def get_movies_by_genre():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({'error': 'No genre provided'}), 400
    
    # Query database for movies matching the genre (case-insensitive)
    movies = Movie.query.filter(Movie.genre.ilike(f"%{genre}%")).all()
    if not movies:
        return jsonify({'error': f'No movies found for genre: {genre}'}), 404

    # Format the movies as a list of dictionaries
    movies_data = [
        {
            'Title': movie.title,
            'Year': movie.year,
            'Genre': movie.genre,
            'Director': movie.director,
            'Actors': movie.actors,
            'imdbRating': movie.imdb_rating,
            'Plot': movie.plot,
            'Poster': movie.poster
        }
        for movie in movies
    ]

    return jsonify({'movies': movies_data})
if __name__ == '__main__':
    app.run(debug=True)
