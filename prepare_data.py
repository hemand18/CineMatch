from config import MOVIES_FILE, CREDITS_FILE
from data_loader import load_movies


def main():

    print("=" * 60)
    print("CineMatch Dataset Validator")
    print("=" * 60)

    if not MOVIES_FILE.exists():
        print(
            f"\n❌ Missing:\n{MOVIES_FILE}"
        )
        return

    if not CREDITS_FILE.exists():
        print(
            f"\n❌ Missing:\n{CREDITS_FILE}"
        )
        return

    print("\nLoading dataset...")

    movies = load_movies()

    print("\n✅ Dataset loaded successfully")

    print(
        f"Movies: {len(movies):,}"
    )

    print(
        f"Columns: {len(movies.columns)}"
    )

    print("\nSample movies:")

    print(
        movies[
            [
                "title",
                "vote_average",
                "release_year"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nDataset is ready for CineMatch.")


if __name__ == "__main__":
    main()