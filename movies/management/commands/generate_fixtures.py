from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
import random
from datetime import datetime, timedelta
import json
import requests
from movies.models import (
    Movie, Genre, Category, MovieVideo, MovieSubtitle,
    Review, Favorite, WatchHistory, Watchlist, Report
)

User = get_user_model()

TMDB_API_KEY = 'fb6e34ebff1505eb93cafca91918b313'  # Replace with your TMDB API key
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

class Command(BaseCommand):
    help = 'Generate fixture data for movies and related models'

    def __init__(self):
        super().__init__()
        self.fake = Faker()
        self.users = []
        self.genres = []
        self.categories = []
        self.movies = []

    def create_users(self, num_users=50):
        self.stdout.write('Creating users...')
        for _ in range(num_users):
            user = User.objects.create(
                email=self.fake.email(),
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                is_active=True
            )
            user.set_password('password123')
            user.save()
            self.users.append(user)

    def create_genres(self):
        self.stdout.write('Creating genres...')
        # Fetch genres from TMDB
        response = requests.get(
            f'{TMDB_BASE_URL}/genre/movie/list',
            params={'api_key': TMDB_API_KEY}
        )
        tmdb_genres = response.json()['genres']
        
        for genre_data in tmdb_genres:
            genre = Genre.objects.create(
                title=genre_data['name'],
                slug=slugify(genre_data['name']),
                description=f"Movies in the {genre_data['name']} genre",
                is_active=True,
                meta_keywords=f"{genre_data['name']}, movies, films",
                meta_description=f"Browse {genre_data['name']} movies"
            )
            self.genres.append(genre)

    def create_categories(self):
        self.stdout.write('Creating categories...')
        categories = [
            'New Releases', 'Trending Now', 'Popular', 'Must Watch',
            'Award Winners', 'Critics Choice', 'Hidden Gems', 'Coming Soon'
        ]
        for idx, name in enumerate(categories):
            category = Category.objects.create(
                name=name,
                slug=slugify(name),
                description=f"Collection of {name.lower()} movies",
                order=idx,
                is_active=True
            )
            self.categories.append(category)

    def fetch_movie_data(self):
        self.stdout.write('Fetching movie data from TMDB...')
        movies_data = []
        page = 1
        
        while len(movies_data) < 200:
            response = requests.get(
                f'{TMDB_BASE_URL}/movie/popular',
                params={
                    'api_key': TMDB_API_KEY,
                    'page': page
                }
            )
            results = response.json()['results']
            if not results:
                break
                
            for movie in results:
                # Fetch detailed movie info
                detail_response = requests.get(
                    f'{TMDB_BASE_URL}/movie/{movie["id"]}',
                    params={'api_key': TMDB_API_KEY}
                )
                if detail_response.status_code == 200:
                    movies_data.append(detail_response.json())
                
                if len(movies_data) >= 200:
                    break
            
            page += 1
        
        return movies_data

    def create_movies(self):
        self.stdout.write('Creating movies...')
        movies_data = self.fetch_movie_data()
        
        for movie_data in movies_data:
            print(movie_data)
            try:
                movie = Movie.objects.create(
                    title=movie_data['title'],
                    original_title=movie_data.get('original_title', ''),
                    slug=f"{slugify(movie_data['title'])}-{random.randint(1000, 9999)}",
                    imdb=float(movie_data['vote_average']),
                    classification=random.choice([0, 12, 16, 18]),
                    year=int(movie_data.get('release_date', '2000')[:4] if movie_data.get('release_date') else '2000'),
                    duration=movie_data.get('runtime', random.randint(90, 180)),
                    description=movie_data.get('overview', ''),
                    downloads=random.randint(0, 10000),
                    views=random.randint(1000, 100000),
                    release_date=movie_data.get('release_date'),
                    director=self.fake.name(),
                    writer=self.fake.name(),
                    trailer_url=f"https://www.youtube.com/watch?v={self.fake.uuid4()}",
                    thumbnail=f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
                    cover=f"https://image.tmdb.org/t/p/w500{movie_data.get('backdrop_path', '')}",
                    is_free=random.choice([True, False]),
                    status='published',
                    featured=random.choice([True, False]),
                    language='English',
                    country=movie_data.get('production_countries', [{}])[0].get('name', 'USA') if movie_data.get('production_countries') else 'USA',
                    budget=movie_data.get('budget', random.randint(1000000, 100000000)),
                    revenue=movie_data.get('revenue', random.randint(1000000, 300000000)),
                    production_company=movie_data.get('production_companies', [{}])[0].get('name', '') if movie_data.get('production_companies') else '',
                    rating_avg=float(movie_data['vote_average']) if movie_data.get('vote_average') else 0,
                    rating_count=int(movie_data['vote_count']) if movie_data.get('vote_count') else 0
                )
            except Exception as e:
                print(e)
                continue
            
            # Add genres
            for genre_data in movie_data.get('genres', []):
                genre = Genre.objects.filter(title=genre_data['name']).first()
                if genre:
                    movie.genres.add(genre)
            
            # Add to random categories
            for category in random.sample(self.categories, random.randint(1, 3)):
                movie.categories.add(category)
            
            self.movies.append(movie)

    def create_movie_videos(self):
        self.stdout.write('Creating movie videos...')
        qualities = ['4K', '1080p', '720p', '480p', '360p']
        
        for movie in self.movies:
            for quality in random.sample(qualities, random.randint(2, 5)):
                MovieVideo.objects.create(
                    movie=movie,
                    title=f"{movie.title} - {quality}",
                    quality=quality,
                    video_url=f"https://example.com/videos/{movie.slug}-{quality}.mp4",
                    size=random.uniform(500.0, 8000.0),
                    encoding_status='completed',
                    duration=movie.duration * 60 if movie.duration else 5400,
                    bitrate=f"{random.randint(1000, 8000)}kbps",
                    codec='H.264'
                )

    def create_interactions(self):
        self.stdout.write('Creating user interactions...')
        
        for movie in self.movies:
            # Create reviews
            num_reviews = random.randint(5, 20)
            for _ in range(num_reviews):
                user = random.choice(self.users)
                try:
                    Review.objects.create(
                        movie=movie,
                        user=user,
                        rating=random.randint(1, 10),
                        comment=self.fake.sentence()
                    )
                except Exception as e:
                    print(e)
                    continue
            
            # Create favorites
            num_favorites = random.randint(10, 50)
            for user in random.sample(self.users, num_favorites):
                try:
                    Favorite.objects.create(
                        movie=movie,
                        user=user
                    )
                except Exception as e:
                    print(e)
                    continue
            
            # Create watch history
            num_watches = min(random.randint(20, 100), len(self.users))
            for user in random.sample(self.users, num_watches):
                WatchHistory.objects.create(
                    movie=movie,
                    user=user,
                    watched_duration=random.randint(0, movie.duration * 60 if movie.duration else 5400),
                    completed=random.choice([True, False])
                )
            
            # Create watchlist entries
            num_watchlist = random.randint(5, 30)
            for user in random.sample(self.users, num_watchlist):
                Watchlist.objects.create(
                    movie=movie,
                    user=user,
                    notes=self.fake.sentence() if random.choice([True, False]) else ''
                )

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting fixture generation...')
        
        # Create base data
        self.create_users()
        self.create_genres()
        self.create_categories()
        
        # Create movies and related data
        self.create_movies()
        self.create_movie_videos()
        self.create_interactions()
        
        self.stdout.write(self.style.SUCCESS('Successfully generated fixture data')) 