import pandas as pd
import numpy as np

# Load the movie ratings data
ratings_data = pd.read_csv('ratings.csv')

# Load the movie titles data
movies_data = pd.read_csv('movies.csv')

# Merge the two datasets
ratings_movies_data = pd.merge(ratings_data, movies_data, on='movieId')

# Calculate the mean rating for each movie
movie_ratings_mean = ratings_movies_data.groupby(['title'])['rating'].mean()

# Create a pivot table for the ratings data
ratings_pivot_table = ratings_movies_data.pivot_table(
    index='userId', columns='title', values='rating')

# Fill the NaN values with zeros
ratings_pivot_table = ratings_pivot_table.fillna(0)

# Define a function to calculate the cosine similarity between two users


def cosine_similarity(user1, user2):
    return np.dot(user1, user2) / (np.linalg.norm(user1) * np.linalg.norm(user2))

# Define a function to calculate the mean-centered rating for a movie


def mean_centered_rating(user_ratings, movie_ratings_mean):
    return user_ratings - movie_ratings_mean

# Define a function to get the top-5 recommended movies for a given movie


def get_top_5_recommendations(movie_title, ratings_pivot_table, movie_ratings_mean):
    # Get the user ratings for the given movie
    movie_ratings = ratings_pivot_table[movie_title]

    # Calculate the mean-centered ratings for all movies
    movie_ratings_centered = ratings_pivot_table.apply(
        lambda x: mean_centered_rating(x, movie_ratings_mean))

    # Calculate the cosine similarity between all users
    similarity_matrix = movie_ratings_centered.apply(
        lambda x: cosine_similarity(x, movie_ratings), axis=1)

    # Sort the similarity scores in descending order and get the top-10 most similar users
    similar_users = similarity_matrix.sort_values(ascending=False)[:10]

    # Get the ratings for the movies that the most similar users have rated
    similar_ratings = ratings_pivot_table.loc[similar_users.index]

    # Calculate the mean rating for each movie
    similar_ratings_mean = similar_ratings.mean()

    # Remove the movies that the current user has already rated
    similar_ratings_mean = similar_ratings_mean.drop(movie_title)

    # Get the top-5 recommended movies
    top_5_recommendations = similar_ratings_mean.sort_values(ascending=False)[
        :5]

    return top_5_recommendations.index.tolist()


# Get input movie from the user
movie_title = input("Enter a movie name: ")

# Get the top-5 recommended movies for the input movie
top_5_recommendations = get_top_5_recommendations(
    movie_title, ratings_pivot_table, movie_ratings_mean)

# Print the top-5 recommended movies
print("Top 5 recommended movies for", movie_title, ":")
for i, recommendation in enumerate(top_5_recommendations):
    print(i+1, recommendation)
