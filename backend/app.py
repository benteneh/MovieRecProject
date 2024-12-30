from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)

# OMDb API details
API_KEY = "6a9cfac6"
BASE_URL = "http://www.omdbapi.com/"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Log SQL statements for debugging
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
    # Force table recreation for debugging purposes
    db.create_all()
    print(f"Database created at {os.path.join(os.getcwd(), 'movies.db')}")

    # Insert a dummy movie record to ensure the database is initialized
    if not Movie.query.first():  # Only insert if the table is empty
        dummy_movie = Movie(
            title="Dummy Movie",
            year="2024",
            genre="Test",
            director="Test Director",
            actors="Test Actor",
            imdb_rating="10.0",
            plot="This is a test movie.",
            poster="N/A"
        )
        db.session.add(dummy_movie)
        db.session.commit()
        print("Inserted dummy record into the movie table.")


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
        return jsonify({'error': 'Please provide a genre'}), 400

    movies = Movie.query.filter(Movie.genre.ilike(f"%{genre}%")).all()  # Case-insensitive search

    if not movies:
        return jsonify({'error': f'No movies found for genre: {genre}'}), 404

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

    return jsonify(movies_data)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)


