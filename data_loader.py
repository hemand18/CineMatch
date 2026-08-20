import ast
import pandas as pd

from config import (
    MOVIES_FILE,
    CREDITS_FILE,
    POSTERS_FILE
)


# =========================================================
# HELPERS
# =========================================================

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def find_column(df, names):
    for name in names:
        if name in df.columns:
            return name
    return None


def parse_json(value):
    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    try:
        return ast.literal_eval(str(value))
    except:
        return []


def extract_names(value):

    data = parse_json(value)

    if not isinstance(data, list):
        return []

    result = []

    for item in data:

        if isinstance(item, dict):

            name = item.get("name")

            if name:
                result.append(str(name))

    return result


def extract_cast(value, limit=5):

    return extract_names(value)[:limit]


def extract_director(value):

    data = parse_json(value)

    if not isinstance(data, list):
        return ""

    for person in data:

        if not isinstance(person, dict):
            continue

        if person.get("job") == "Director":

            return str(
                person.get("name", "")
            )

    return ""


# =========================================================
# POSTER URL
# =========================================================

def build_poster_url(value):

    if pd.isna(value):
        return ""

    value = str(value).strip()

    if not value:
        return ""

    if value.lower() in [
        "nan",
        "none",
        "null"
    ]:
        return ""

    # Already a complete URL
    if value.startswith("http://"):
        return value

    if value.startswith("https://"):
        return value

    # TMDB poster path
    if value.startswith("/"):
        return (
            "https://image.tmdb.org/t/p/w500"
            + value
        )

    # Just poster filename/path
    return (
        "https://image.tmdb.org/t/p/w500/"
        + value
    )


# =========================================================
# LOAD MOVIES
# =========================================================

def load_movies():

    print("\n" + "=" * 60)
    print("🎬 CineMatch Dataset Loader")
    print("=" * 60)


    # =====================================================
    # MOVIES.CSV
    # =====================================================

    print("\n📂 Loading movies.csv...")

    movies = pd.read_csv(
        MOVIES_FILE
    )

    movies = clean_columns(
        movies
    )

    print(
        f"✅ Movies loaded: {len(movies):,}"
    )

    print(
        "Movie columns:",
        list(movies.columns)
    )


    # =====================================================
    # MOVIE ID
    # =====================================================

    movie_id_column = find_column(
        movies,
        [
            "id",
            "movie_id",
            "tmdb_id",
            "movieid"
        ]
    )

    if movie_id_column is None:

        raise ValueError(
            "Movie ID column not found in movies.csv.\n"
            f"Available columns: {list(movies.columns)}"
        )


    if movie_id_column != "id":

        movies = movies.rename(
            columns={
                movie_id_column: "id"
            }
        )


    # =====================================================
    # STANDARD COLUMNS
    # =====================================================

    rename_map = {

        "original_title": "title",

        "movie_title": "title",

        "description": "overview",

        "plot": "overview",

        "rating": "vote_average",

        "rating_average": "vote_average",

        "votes": "vote_count",

        "vote_counts": "vote_count",

        "year": "release_year"

    }


    for old, new in rename_map.items():

        if (
            old in movies.columns
            and new not in movies.columns
        ):

            movies = movies.rename(
                columns={
                    old: new
                }
            )


    # =====================================================
    # DEFAULT COLUMNS
    # =====================================================

    defaults = {

        "title": "",

        "genres": "",

        "keywords": "",

        "overview": "",

        "popularity": 0,

        "vote_average": 0,

        "vote_count": 0,

        "release_date": ""

    }


    for column, default in defaults.items():

        if column not in movies.columns:

            movies[column] = default


    # =====================================================
    # CREDITS.CSV
    # =====================================================

    print("\n📂 Loading credits.csv...")

    credits = pd.read_csv(
        CREDITS_FILE
    )

    credits = clean_columns(
        credits
    )

    print(
        f"✅ Credits loaded: {len(credits):,}"
    )

    print(
        "Credit columns:",
        list(credits.columns)
    )


    credit_id_column = find_column(
        credits,
        [
            "id",
            "movie_id",
            "tmdb_id",
            "movieid"
        ]
    )


    if credit_id_column is None:

        raise ValueError(
            "Movie ID column not found in credits.csv.\n"
            f"Available columns: {list(credits.columns)}"
        )


    if credit_id_column != "id":

        credits = credits.rename(
            columns={
                credit_id_column: "id"
            }
        )


    # =====================================================
    # CAST / CREW
    # =====================================================

    cast_column = find_column(
        credits,
        [
            "cast",
            "actors",
            "actor"
        ]
    )


    crew_column = find_column(
        credits,
        [
            "crew",
            "staff"
        ]
    )


    if cast_column is None:

        credits["cast"] = ""

    elif cast_column != "cast":

        credits = credits.rename(
            columns={
                cast_column: "cast"
            }
        )


    if crew_column is None:

        credits["crew"] = ""

    elif crew_column != "crew":

        credits = credits.rename(
            columns={
                crew_column: "crew"
            }
        )


    credits = credits[
        [
            "id",
            "cast",
            "crew"
        ]
    ]


    credits = credits.drop_duplicates(
        subset=["id"]
    )


    # =====================================================
    # STANDARDIZE IDS
    # =====================================================

    movies["id"] = (
        movies["id"]
        .astype(str)
        .str.strip()
    )


    credits["id"] = (
        credits["id"]
        .astype(str)
        .str.strip()
    )


    # =====================================================
    # MERGE MOVIES + CREDITS
    # =====================================================

    print(
        "\n🔗 Merging movies + credits..."
    )

    movies = movies.merge(
        credits,
        on="id",
        how="left"
    )

    print(
        "✅ Movies + credits merged"
    )


    # =====================================================
    # POSTER.CSV
    # =====================================================

    print(
        "\n📂 Loading poster.csv..."
    )

    posters = pd.read_csv(
        POSTERS_FILE
    )

    posters = clean_columns(
        posters
    )

    print(
        f"✅ Posters loaded: {len(posters):,}"
    )

    print(
        "Poster columns:",
        list(posters.columns)
    )


    # =====================================================
    # POSTER TITLE
    # =====================================================

    poster_title_column = find_column(
        posters,
        [
            "title",
            "movie_title",
            "original_title",
            "name"
        ]
    )


    if poster_title_column is None:

        raise ValueError(
            "❌ Movie title column not found in poster.csv.\n\n"
            f"Available columns:\n"
            f"{list(posters.columns)}"
        )


    # =====================================================
    # POSTER COLUMN
    # =====================================================

    poster_column = find_column(
        posters,
        [
            "poster",
            "poster_path",
            "poster_url",
            "image_url",
            "image_path",
            "image",
            "url"
        ]
    )


    if poster_column is None:

        raise ValueError(
            "❌ Poster column not found in poster.csv.\n\n"
            f"Available columns:\n"
            f"{list(posters.columns)}"
        )


    # =====================================================
    # RENAME
    # =====================================================

    posters = posters.rename(
        columns={
            poster_title_column: "poster_title",
            poster_column: "poster_path"
        }
    )


    # =====================================================
    # CLEAN TITLES
    # =====================================================

    posters["poster_title_clean"] = (
        posters["poster_title"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


    movies["title_clean"] = (
        movies["title"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # =====================================================
    # POSTER URL
    # =====================================================

    posters["poster_path"] = (
        posters["poster_path"]
        .apply(
            build_poster_url
        )
    )


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    posters = posters.drop_duplicates(
        subset=["poster_title_clean"]
    )


    # =====================================================
    # MERGE POSTERS USING TITLE
    # =====================================================

    print(
        "\n🔗 Matching posters with movies..."
    )


    movies = movies.merge(

        posters[
            [
                "poster_title_clean",
                "poster_path"
            ]
        ],

        left_on="title_clean",

        right_on="poster_title_clean",

        how="left"

    )


    # =====================================================
    # POSTER STATS
    # =====================================================

    movies["poster_path"] = (
        movies["poster_path"]
        .fillna("")
        .astype(str)
    )


    poster_count = (
        movies["poster_path"]
        .str.startswith("http")
        .sum()
    )


    print(
        f"✅ Posters matched: {poster_count:,}"
    )


    # =====================================================
    # GENRES
    # =====================================================

    movies["genres_list"] = (
        movies["genres"]
        .apply(
            extract_names
        )
    )


    # =====================================================
    # KEYWORDS
    # =====================================================

    movies["keywords_list"] = (
        movies["keywords"]
        .apply(
            extract_names
        )
    )


    # =====================================================
    # CAST
    # =====================================================

    movies["cast_list"] = (
        movies["cast"]
        .fillna("")
        .apply(
            extract_cast
        )
    )


    # =====================================================
    # DIRECTOR
    # =====================================================

    movies["director"] = (
        movies["crew"]
        .fillna("")
        .apply(
            extract_director
        )
    )


    # =====================================================
    # RELEASE YEAR
    # =====================================================

    if "release_year" not in movies.columns:

        movies["release_year"] = (
            pd.to_datetime(
                movies["release_date"],
                errors="coerce"
            )
            .dt.year
        )


    # =====================================================
    # NUMERIC COLUMNS
    # =====================================================

    movies["vote_average"] = pd.to_numeric(
        movies["vote_average"],
        errors="coerce"
    ).fillna(0)


    movies["vote_count"] = pd.to_numeric(
        movies["vote_count"],
        errors="coerce"
    ).fillna(0)


    movies["popularity"] = pd.to_numeric(
        movies["popularity"],
        errors="coerce"
    ).fillna(0)


    # =====================================================
    # CLEAN
    # =====================================================

    movies = movies.drop_duplicates(
        subset=["id"]
    )


    movies = movies.reset_index(
        drop=True
    )


    # =====================================================
    # FINAL REPORT
    # =====================================================

    print(
        "\n" + "=" * 60
    )

    print(
        "🎬 CineMatch Dataset Ready"
    )

    print(
        "=" * 60
    )

    print(
        f"🎥 Movies: {len(movies):,}"
    )

    print(
        f"🖼️ Posters matched: {poster_count:,}"
    )

    print(
        f"🎭 Cast available: "
        f"{movies['cast_list'].apply(len).gt(0).sum():,}"
    )

    print(
        f"🎬 Directors available: "
        f"{movies['director'].ne('').sum():,}"
    )

    print(
        "=" * 60
    )


    return movies