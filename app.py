import pandas as pd
import streamlit as st

from data_loader import load_movies
from recommender import CineMatchRecommender
from config import APP_NAME


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title=APP_NAME,

    page_icon="🎬",

    layout="wide",

    initial_sidebar_state="collapsed"

)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {

    font-family: 'Inter', sans-serif;

}

.stApp {

    background:

    radial-gradient(
        circle at 20% 10%,
        rgba(124,58,237,0.18),
        transparent 30%
    ),

    radial-gradient(
        circle at 80% 20%,
        rgba(59,130,246,0.10),
        transparent 25%
    ),

    #08090d;

    color:#f8fafc;

}

.block-container {

    max-width:1400px;

    padding-top:1.5rem;

    padding-bottom:4rem;

}

.hero {

    padding:3rem;

    border-radius:28px;

    background:

    linear-gradient(
        135deg,
        rgba(124,58,237,0.20),
        rgba(15,23,42,0.85)
    );

    border:1px solid
    rgba(255,255,255,0.08);

    margin-bottom:2rem;

}

.main-title {

    font-size:3.2rem;

    font-weight:800;

    letter-spacing:-2px;

}

.gradient-text {

    background:

    linear-gradient(
        90deg,
        #c084fc,
        #818cf8,
        #38bdf8
    );

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

}

.subtitle {

    color:#94a3b8;

    font-size:1.05rem;

    margin-top:0.5rem;

}

.section-title {

    font-size:1.5rem;

    font-weight:700;

    margin-top:2rem;

    margin-bottom:1rem;

}

.movie-title {

    font-size:0.95rem;

    font-weight:700;

    margin-top:8px;

}

.movie-meta {

    color:#94a3b8;

    font-size:0.78rem;

}

.rating {

    color:#fbbf24;

    font-weight:700;

}

.score {

    display:inline-block;

    padding:4px 8px;

    border-radius:999px;

    background:
    rgba(168,85,247,0.15);

    color:#d8b4fe;

    font-size:0.75rem;

    font-weight:700;

}

.details-card {

    background:
    rgba(17,19,26,0.92);

    border:1px solid
    rgba(255,255,255,0.08);

    border-radius:24px;

    padding:25px;

}

.detail-title {

    font-size:2rem;

    font-weight:800;

}

.detail-text {

    color:#cbd5e1;

    line-height:1.7;

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# DATA
# =========================================================

@st.cache_data(
    show_spinner=False
)
def get_movies():

    return load_movies()


@st.cache_resource(
    show_spinner=False
)
def get_recommender():

    movies = get_movies()

    return CineMatchRecommender(
        movies
    )


try:

    with st.spinner(
        "Loading CineMatch AI..."
    ):

        movies = get_movies()

        recommender = get_recommender()


except Exception as error:

    st.error(
        "Unable to load the movie dataset."
    )

    st.code(
        str(error)
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div style="
display:flex;
align-items:center;
justify-content:space-between;
margin-bottom:1rem;
">

<div>

<span style="
font-size:1.5rem;
font-weight:800;
">

🎬 CineMatch

</span>

</div>

<div style="
color:#94a3b8;
font-size:0.9rem;
">

AI Movie Recommendation System

</div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">

<div class="main-title">

Find your next
<span class="gradient-text">
favorite movie
</span>

</div>

<div class="subtitle">

Discover movies using AI-powered recommendations
based on genres, plot, keywords, cast and directors.

</div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# SEARCH
# =========================================================

movie_titles = (
    movies["title"]
    .dropna()
    .astype(str)
    .sort_values()
    .tolist()
)


search_col, button_col = st.columns(
    [5, 1]
)


with search_col:

    selected_movie = st.selectbox(

        "Search movie",

        movie_titles,

        index=None,

        placeholder="🔎 Search for a movie..."

    )


with button_col:

    st.write("")

    recommend_clicked = st.button(

        "Recommend",

        type="primary",

        use_container_width=True

    )


# =========================================================
# SESSION STATE
# =========================================================

if "selected_movie" not in st.session_state:

    st.session_state.selected_movie = None


if "recommendations" not in st.session_state:

    st.session_state.recommendations = None


if recommend_clicked:

    if not selected_movie:

        st.warning(
            "Please select a movie first."
        )

    else:

        with st.spinner(
            "Finding movies you'll love..."
        ):

            results = recommender.recommend(

                selected_movie,

                num_recommendations=10

            )


        st.session_state.selected_movie = (
            selected_movie
        )

        st.session_state.recommendations = (
            results
        )


# =========================================================
# SELECTED MOVIE
# =========================================================

if st.session_state.selected_movie:

    selected_title = (
        st.session_state.selected_movie
    )


    selected_index = (
        recommender.find_movie(
            selected_title
        )
    )


    if selected_index is not None:

        selected = movies.iloc[
            selected_index
        ]


        st.markdown(
            '<div class="section-title">'
            '🎬 Selected Movie'
            '</div>',
            unsafe_allow_html=True
        )


        poster = selected.get(
            "poster_path",
            ""
        )


        col1, col2 = st.columns(
            [1, 3]
        )


        with col1:

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.info(
                    "🎬 Poster unavailable"
                )


        with col2:

            year = selected.get(
                "release_year"
            )


            if pd.notna(year):

                year_text = str(
                    int(year)
                )

            else:

                year_text = "N/A"


            st.markdown(
                f"""
<div class="details-card">

<div class="detail-title">

{selected['title']}

</div>

<br>

<span class="rating">

⭐ {selected['vote_average']:.1f}

</span>

&nbsp;&nbsp;

<span class="movie-meta">

📅 {year_text}

</span>

<br><br>

<div class="detail-text">

{selected['overview']
if selected['overview']
else 'No overview available.'}

</div>

</div>
""",
                unsafe_allow_html=True
            )


# =========================================================
# RECOMMENDATIONS
# =========================================================

results = (
    st.session_state.recommendations
)


if results is not None and not results.empty:

    st.markdown(
        '<div class="section-title">'
        '✨ Recommended for You'
        '</div>',
        unsafe_allow_html=True
    )


    for start in range(
        0,
        len(results),
        5
    ):

        row = results.iloc[
            start:start + 5
        ]


        columns = st.columns(
            len(row)
        )


        for column, (_, movie) in zip(
            columns,
            row.iterrows()
        ):

            with column:

                poster = movie.get(
                    "poster_path",
                    ""
                )


                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "🎬 No poster"
                    )


                year = movie.get(
                    "release_year"
                )


                if pd.notna(year):

                    year_text = str(
                        int(year)
                    )

                else:

                    year_text = "N/A"


                st.markdown(
                    f"""
<div class="movie-title">

{movie['title']}

</div>

<div class="movie-meta">

<span class="rating">

⭐ {movie['vote_average']:.1f}

</span>

&nbsp;•&nbsp;

{year_text}

</div>

<br>

<span class="score">

{movie['similarity_percent']:.0f}% Match

</span>

""",
                    unsafe_allow_html=True
                )


    # =====================================================
    # EXPLANATION
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🧠 Why These Movies?'
        '</div>',
        unsafe_allow_html=True
    )


    st.info(
        "CineMatch combines plot similarity, "
        "genres, keywords, cast, director, "
        "ratings, popularity and vote confidence "
        "to rank recommendations."
    )


    # =====================================================
    # ANALYSIS
    # =====================================================

    with st.expander(
        "📊 View recommendation analysis"
    ):

        display_results = results[
            [
                "title",
                "vote_average",
                "similarity_percent",
                "reason"
            ]
        ].copy()


        display_results.columns = [

            "Movie",

            "Rating",

            "Similarity",

            "Why Recommended"

        ]


        display_results[
            "Similarity"
        ] = (

            display_results[
                "Similarity"
            ].round(1).astype(str)

            + "%"

        )


        st.dataframe(

            display_results,

            use_container_width=True,

            hide_index=True

        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<br><br>

<div style="
text-align:center;
color:#64748b;
padding:2rem;
border-top:1px solid rgba(255,255,255,0.06);
">

🎬 <b>CineMatch</b>

<br>

AI-Powered Movie Recommendation System

<br><br>

Built with Python • Pandas • Scikit-learn • Streamlit

</div>
""",
    unsafe_allow_html=True
)