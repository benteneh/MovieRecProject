import requests
from app import app, db, Movie

API_KEY = "6a9cfac6"
BASE_URL = "http://www.omdbapi.com/"

def fetch_and_add_movies_by_genre(genre, pages=1):
    for page in range(1, pages + 1):
        params = {'apikey': API_KEY, 's': genre, 'type': 'movie', 'page': page}
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                for movie_data in data.get('Search', []):
                    fetch_and_add_movie(movie_data['Title'])
            else:
                print(f"No results for genre: {genre}")
        else:
            print(f"Failed to fetch movies for genre: {genre}")

def fetch_and_add_movie(title):
    params = {'apikey': API_KEY, 't': title}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            if not Movie.query.filter_by(title=data.get('Title')).first():
                movie = Movie(
                    title=data.get('Title'),
                    year=data.get('Year'),
                    genre=data.get('Genre'),
                    director=data.get('Director'),
                    actors=data.get('Actors'),
                    imdb_rating=data.get('imdbRating'),
                    plot=data.get('Plot'),
                    poster=data.get('Poster')
                )
                db.session.add(movie)
                db.session.commit()
                print(f"Added: {data.get('Title')}")
            else:
                print(f"Movie already exists: {data.get('Title')}")
        else:
            print(f"Movie not found: {title}")
    else:
        print(f"Failed to fetch: {title}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database schema is initialized

        # Fetch movies by genre
        genres = ["Horror", "Sci-Fi", "Romance", "Thriller"]
        for genre in genres:
            print(f"Fetching movies for genre: {genre}")
            fetch_and_add_movies_by_genre(genre, pages=5)  # Fetch 2 pages per genre

