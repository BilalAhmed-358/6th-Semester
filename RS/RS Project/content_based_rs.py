import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def content_based_filtering(movieName):
    movies_df = pd.read_csv(
        r'C:\Users\Bilal\Desktop\RS assignment\ml-latest-small\movies.csv')

    vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
    genre_matrix = vectorizer.fit_transform(movies_df['genres'])

    genre_similarity = cosine_similarity(genre_matrix)

    def recommend_movies(movie_name, n_recommendations):
        movie_index = movies_df.loc[movies_df['title'] == movie_name].index[0]

        movie_scores = genre_similarity[movie_index]

        top_movies = movie_scores.argsort()[::-1][1:n_recommendations+1]

        return movies_df.loc[top_movies, 'title'].tolist()

    movie_name = movieName
    n_recommendations = 5
    recommendations = recommend_movies(movie_name, n_recommendations)
    return recommendations
