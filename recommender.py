import re

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import (
    CONTENT_WEIGHT,
    RATING_WEIGHT,
    POPULARITY_WEIGHT,
    VOTE_WEIGHT
)


class CineMatchRecommender:

    def __init__(self, movies):

        self.movies = movies.copy()

        self.vectorizer = None

        self.tfidf_matrix = None

        self.similarity_matrix = None

        self.prepare_data()

        self.build_model()


    # =====================================================
    # PREPARE DATA
    # =====================================================

    def prepare_data(self):

        df = self.movies


        def list_to_text(value):

            if isinstance(value, list):

                return " ".join(
                    str(x).lower()
                    for x in value
                )

            return str(
                value
            ).lower()


        df["genres_text"] = (
            df["genres_list"]
            .apply(list_to_text)
        )


        df["keywords_text"] = (
            df["keywords_list"]
            .apply(list_to_text)
        )


        df["cast_text"] = (
            df["cast_list"]
            .apply(list_to_text)
        )


        df["director_text"] = (
            df["director"]
            .fillna("")
            .astype(str)
            .str.lower()
        )


        df["overview_text"] = (
            df["overview"]
            .fillna("")
            .astype(str)
            .str.lower()
        )


        # Give genres and keywords extra importance

        df["combined_features"] = (

            df["genres_text"] + " " +

            df["genres_text"] + " " +

            df["keywords_text"] + " " +

            df["keywords_text"] + " " +

            df["cast_text"] + " " +

            df["director_text"] + " " +

            df["overview_text"]

        )


        df["combined_features"] = (
            df["combined_features"]
            .apply(
                self.clean_text
            )
        )


        # Rating

        df["rating_normalized"] = (
            df["vote_average"] / 10
        )


        # Popularity

        popularity_log = np.log1p(
            df["popularity"]
        )


        max_popularity = (
            popularity_log.max()
        )


        if max_popularity > 0:

            df["popularity_normalized"] = (
                popularity_log
                /
                max_popularity
            )

        else:

            df["popularity_normalized"] = 0


        # Vote confidence

        max_votes = (
            df["vote_count"].max()
        )


        if max_votes > 0:

            df["vote_normalized"] = (

                np.log1p(
                    df["vote_count"]
                )

                /

                np.log1p(
                    max_votes
                )

            )

        else:

            df["vote_normalized"] = 0


        self.movies = df


    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @staticmethod
    def clean_text(text):

        text = str(text).lower()

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()


    # =====================================================
    # BUILD MODEL
    # =====================================================

    def build_model(self):

        print(
            "\n🧠 Building CineMatch AI model..."
        )


        self.vectorizer = TfidfVectorizer(

            stop_words="english",

            max_features=20000,

            ngram_range=(1, 2),

            min_df=2

        )


        self.tfidf_matrix = (
            self.vectorizer.fit_transform(
                self.movies[
                    "combined_features"
                ]
            )
        )


        print(
            "✅ TF-IDF model created"
        )


        self.similarity_matrix = (
            cosine_similarity(
                self.tfidf_matrix
            )
        )


        print(
            "✅ Similarity matrix created"
        )


        print(
            "🎬 CineMatch AI model ready!"
        )


    # =====================================================
    # FIND MOVIE
    # =====================================================

    def find_movie(
        self,
        movie_title
    ):

        movie_title = (
            str(movie_title)
            .strip()
            .lower()
        )


        exact = self.movies[
            self.movies["title"]
            .fillna("")
            .str.lower()
            .eq(movie_title)
        ]


        if not exact.empty:

            return exact.index[0]


        partial = self.movies[
            self.movies["title"]
            .fillna("")
            .str.lower()
            .str.contains(
                movie_title,
                regex=False
            )
        ]


        if not partial.empty:

            return partial.index[0]


        return None


    # =====================================================
    # RECOMMEND
    # =====================================================

    def recommend(
        self,
        movie_title,
        num_recommendations=10
    ):

        movie_index = self.find_movie(
            movie_title
        )


        if movie_index is None:

            return pd.DataFrame()


        content_scores = (
            self.similarity_matrix[
                movie_index
            ].copy()
        )


        rating_scores = (
            self.movies[
                "rating_normalized"
            ].values
        )


        popularity_scores = (
            self.movies[
                "popularity_normalized"
            ].values
        )


        vote_scores = (
            self.movies[
                "vote_normalized"
            ].values
        )


        final_scores = (

            CONTENT_WEIGHT
            * content_scores

            +

            RATING_WEIGHT
            * rating_scores

            +

            POPULARITY_WEIGHT
            * popularity_scores

            +

            VOTE_WEIGHT
            * vote_scores

        )


        # Remove selected movie

        final_scores[
            movie_index
        ] = -1


        top_indices = np.argsort(
            final_scores
        )[::-1][
            :num_recommendations
        ]


        recommendations = (
            self.movies
            .iloc[top_indices]
            .copy()
        )


        recommendations[
            "content_similarity"
        ] = content_scores[
            top_indices
        ]


        recommendations[
            "final_score"
        ] = final_scores[
            top_indices
        ]


        recommendations[
            "similarity_percent"
        ] = np.clip(
            recommendations[
                "content_similarity"
            ] * 100,
            0,
            100
        )


        selected = (
            self.movies.iloc[
                movie_index
            ]
        )


        recommendations[
            "reason"
        ] = recommendations.apply(

            lambda row:
            self.generate_reason(
                selected,
                row
            ),

            axis=1

        )


        return recommendations


    # =====================================================
    # EXPLANATION
    # =====================================================

    def generate_reason(
        self,
        selected,
        recommended
    ):

        reasons = []


        selected_genres = set(
            selected.get(
                "genres_list",
                []
            )
        )


        recommended_genres = set(
            recommended.get(
                "genres_list",
                []
            )
        )


        if (
            selected_genres
            &
            recommended_genres
        ):

            reasons.append(
                "similar genres"
            )


        selected_keywords = set(
            selected.get(
                "keywords_list",
                []
            )
        )


        recommended_keywords = set(
            recommended.get(
                "keywords_list",
                []
            )
        )


        if (
            selected_keywords
            &
            recommended_keywords
        ):

            reasons.append(
                "similar themes"
            )


        selected_cast = set(
            selected.get(
                "cast_list",
                []
            )
        )


        recommended_cast = set(
            recommended.get(
                "cast_list",
                []
            )
        )


        if (
            selected_cast
            &
            recommended_cast
        ):

            reasons.append(
                "shared cast"
            )


        selected_director = str(
            selected.get(
                "director",
                ""
            )
        ).strip().lower()


        recommended_director = str(
            recommended.get(
                "director",
                ""
            )
        ).strip().lower()


        if (
            selected_director
            and
            selected_director
            ==
            recommended_director
        ):

            reasons.append(
                "same director"
            )


        if not reasons:

            reasons.append(
                "similar plot and movie characteristics"
            )


        return (
            "Recommended because of "
            + ", ".join(reasons)
            + "."
        )