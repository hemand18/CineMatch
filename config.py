from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MOVIES_FILE = DATA_DIR / "movies.csv"
CREDITS_FILE = DATA_DIR / "credits.csv"
POSTERS_FILE = DATA_DIR / "poster.csv"

APP_NAME = "CineMatch"

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

DEFAULT_RECOMMENDATIONS = 10

CONTENT_WEIGHT = 0.65
RATING_WEIGHT = 0.15
POPULARITY_WEIGHT = 0.10
VOTE_WEIGHT = 0.10