import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def content_based_filtering(user_id):
    ratings_df = pd.read_csv(
        r'C:\Users\Bilal\Desktop\RS assignment\ml-latest-small\ratings.csv')

    # Filter ratings for the given user ID
    user_ratings = ratings_df[ratings_df['userId'] == user_id]

    # Get unique movie IDs rated by the user
    movie_ids = user_ratings['movieId'].unique()

    movies_df = pd.read_csv(
        r'C:\Users\Bilal\Desktop\RS assignment\ml-latest-small\movies.csv')

    # Filter movies based on the user's rated movie IDs
    user_movies = movies_df[movies_df['movieId'].isin(movie_ids)]

    vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
    genre_matrix = vectorizer.fit_transform(user_movies['genres'])

    genre_similarity = cosine_similarity(genre_matrix)

    def recommend_movies(movie_index, n_recommendations):
        movie_scores = genre_similarity[movie_index]

        top_movies = movie_scores.argsort()[::-1][1:n_recommendations+1]

        return movies_df.loc[top_movies, 'title'].tolist()

    n_recommendations = 5
    if len(user_movies) > 0:
        movie_index = user_movies.index[0]
        recommendations = recommend_movies(movie_index, n_recommendations)
        return recommendations
    else:
        return "No recommendations available for the user."


# user_id = int(input("Enter a user ID: "))
# recommendations = content_based_filtering(user_id)
# print(recommendations)
