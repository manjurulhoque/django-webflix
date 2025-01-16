from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
import random
from datetime import datetime, timedelta
import requests
from series.models import (
    Series, Season, Episode, EpisodeVideo, EpisodeSubtitle,
    SeriesReview, VideoQualityChoices, SeriesStatusChoices
)
from genres.models import Genre

User = get_user_model()

TMDB_API_KEY = 'fb6e34ebff1505eb93cafca91918b313'  # Replace with your TMDB API key
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

class Command(BaseCommand):
    help = 'Generate fixture data for TV series from TMDB'

    def __init__(self):
        super().__init__()
        self.fake = Faker()
        self.users = list(User.objects.all())
        self.genres = list(Genre.objects.all())

    def fetch_series_data(self):
        self.stdout.write('Fetching TV series data from TMDB...')
        series_data = []
        page = 1
        
        while len(series_data) < 200:
            response = requests.get(
                f'{TMDB_BASE_URL}/tv/popular',
                params={
                    'api_key': TMDB_API_KEY,
                    'page': page
                }
            )
            results = response.json().get('results', [])
            if not results:
                break
                
            for series in results:
                # Fetch detailed series info
                detail_response = requests.get(
                    f'{TMDB_BASE_URL}/tv/{series["id"]}',
                    params={'api_key': TMDB_API_KEY}
                )
                if detail_response.status_code == 200:
                    series_data.append(detail_response.json())
                
                if len(series_data) >= 200:
                    break
            
            page += 1
        
        return series_data

    def create_series(self):
        self.stdout.write('Creating TV series...')
        series_data = self.fetch_series_data()
        
        for data in series_data:
            try:
                series = Series.objects.create(
                    title=data['name'],
                    original_title=data.get('original_name', ''),
                    slug=slugify(f"{data['name']}-{random.randint(1000, 9999)}"),
                    description=data.get('overview', ''),
                    year=int(data.get('first_air_date', '2000')[:4]),
                    imdb=float(data['vote_average']) if data.get('vote_average') else 0.0,
                    classification=random.choice([0, 12, 16, 18]),
                    thumbnail=f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}",
                    cover=f"https://image.tmdb.org/t/p/original{data.get('backdrop_path', '')}",
                    trailer_url=f"https://www.youtube.com/watch?v={self.fake.uuid4()}",
                    status=SeriesStatusChoices.PUBLISHED,
                    featured=random.choice([True, False]),
                    views=random.randint(1000, 100000),
                    is_free=random.choice([True, False]),
                    language=data.get('original_language', 'en').upper(),
                    country=data.get('origin_country', ['US'])[0],
                    network=data.get('networks', [{}])[0].get('name', 'Unknown Network') if data.get('networks') else 'Unknown Network',
                    total_seasons=len(data.get('seasons', [])),
                    release_date=datetime.strptime(data['first_air_date'], '%Y-%m-%d').date() if data.get('first_air_date') else datetime.now().date(),
                    end_date=datetime.strptime(data['last_air_date'], '%Y-%m-%d').date() if data.get('last_air_date') else None,
                )

                # Add genres
                for genre_data in data.get('genres', []):
                    genre = Genre.objects.filter(title=genre_data['name']).first()
                    if genre:
                        series.genres.add(genre)

                # Create seasons and episodes
                self.create_seasons_and_episodes(series, data.get('seasons', []))
                
                # Create reviews
                self.create_series_reviews(series)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating series {data.get("name")}: {str(e)}'))
                continue

    def create_seasons_and_episodes(self, series, seasons_data):
        for season_data in seasons_data:
            if season_data['season_number'] == 0:  # Skip specials
                continue
                
            season = Season.objects.create(
                series=series,
                number=season_data['season_number'],
                title=season_data.get('name', f'Season {season_data["season_number"]}'),
                description=season_data.get('overview', ''),
                poster=f"https://image.tmdb.org/t/p/w500{season_data.get('poster_path', '')}",
                release_date=datetime.strptime(season_data['air_date'], '%Y-%m-%d').date() if season_data.get('air_date') else series.release_date,
            )

            # Create episodes
            self.create_episodes(season, season_data.get('episode_count', random.randint(8, 13)))

    def create_episodes(self, season, episode_count):
        for ep_num in range(1, episode_count + 1):
            episode = Episode.objects.create(
                season=season,
                number=ep_num,
                title=self.fake.sentence(nb_words=4),
                description=self.fake.paragraph(),
                duration=random.randint(20, 60),
                thumbnail=f"https://picsum.photos/500/281?random={random.randint(1, 1000)}",
                release_date=season.release_date + timedelta(days=ep_num * 7),
                views=random.randint(100, 10000),
                is_free=season.series.is_free,
                status=SeriesStatusChoices.PUBLISHED,
            )

            # Create video qualities
            self.create_episode_videos(episode)
            
            # Create subtitles
            self.create_episode_subtitles(episode)

    def create_episode_videos(self, episode):
        qualities = list(VideoQualityChoices)
        for quality in random.sample(qualities, random.randint(2, len(qualities))):
            EpisodeVideo.objects.create(
                episode=episode,
                title=f"{episode.title} - {quality[1]}",
                quality=quality[0],
                video_url=f"https://example.com/videos/{episode.season.series.slug}/s{episode.season.number:02d}e{episode.number:02d}-{quality[0]}.mp4",
                size=random.uniform(500.0, 8000.0),
                duration=episode.duration * 60,
                codec='H.264',
                bitrate=f"{random.randint(1000, 8000)}kbps",
            )

    def create_episode_subtitles(self, episode):
        languages = ['English', 'Spanish', 'French', 'German', 'Italian']
        for lang in random.sample(languages, random.randint(1, len(languages))):
            EpisodeSubtitle.objects.create(
                episode=episode,
                language=lang,
                subtitle_url=f"https://example.com/subtitles/{episode.season.series.slug}/s{episode.season.number:02d}e{episode.number:02d}-{lang.lower()}.srt",
            )

    def create_series_reviews(self, series):
        num_reviews = random.randint(5, 20)
        for _ in range(num_reviews):
            try:
                SeriesReview.objects.create(
                    series=series,
                    user=random.choice(self.users),
                    rating=random.randint(1, 10),
                    comment=self.fake.paragraph(),
                )
            except Exception:
                continue

    def handle(self, *args, **kwargs):
        if not self.users:
            self.stdout.write(self.style.ERROR('No users found. Please create some users first.'))
            return
            
        if not self.genres:
            self.stdout.write(self.style.ERROR('No genres found. Please create genres first.'))
            return

        self.stdout.write('Starting TV series generation...')
        self.create_series()
        self.stdout.write(self.style.SUCCESS('Successfully generated TV series data')) 