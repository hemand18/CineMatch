# 🎬 CineMatch

## AI-Powered Movie Recommendation System

CineMatch is an end-to-end machine learning project that recommends movies based on content similarity and movie quality signals.

The application combines NLP, TF-IDF vectorization, cosine similarity and hybrid ranking to generate movie recommendations.

---

## 🚀 Features

- Movie search
- Top 10 movie recommendations
- TF-IDF based NLP
- Cosine similarity
- Genre matching
- Keyword matching
- Cast matching
- Director matching
- Plot similarity
- Rating adjustment
- Popularity adjustment
- Vote confidence
- Recommendation explanation
- Movie posters
- Professional dark UI
- Cached ML model
- Streamlit deployment

---

## 🧠 Machine Learning Pipeline

Movie metadata

↓

Feature engineering

↓

Genres + Keywords + Cast + Director + Overview

↓

TF-IDF Vectorization

↓

Cosine Similarity

↓

Content Similarity Score

↓

Rating + Popularity + Vote Confidence

↓

Hybrid Ranking

↓

Top 10 Recommendations

---

## 🛠 Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- NLP
- TF-IDF
- Cosine Similarity
- GitHub

---

## 📂 Project Structure

CineMatch/

├── app.py

├── recommender.py

├── data_loader.py

├── prepare_data.py

├── config.py

├── requirements.txt

├── README.md

├── .gitignore

├── data/

│   ├── tmdb_5000_movies.csv

│   └── tmdb_5000_credits.csv

└── .streamlit/

    └── config.toml

---

## ▶️ Run Locally

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Move into the project:

cd CineMatch

Install dependencies:

pip install -r requirements.txt

Validate the dataset:

python prepare_data.py

Run the application:

streamlit run app.py

---

## 📊 Recommendation Formula

The final recommendation score combines several signals:

Content Similarity = 65%

Rating = 15%

Popularity = 10%

Vote Confidence = 10%

Final Score:

0.65 × Content Similarity

+

0.15 × Rating

+

0.10 × Popularity

+

0.10 × Vote Confidence

---

## 🔍 Explainability

CineMatch explains recommendations using:

- Genre overlap
- Shared cast
- Same director
- Plot similarity
- Keywords

This makes the recommendation engine easier to understand.

---

## ☁️ Deployment

CineMatch can be deployed using Streamlit Community Cloud.

Select:

Repository: your GitHub repository

Branch: main

Main file:

app.py

---

## 👨‍💻 Author

Your Name

Data Analyst | Data Science | Machine Learning

---

## 📜 License

This project is intended for educational and portfolio purposes.