import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import KBinsDiscretizer


def naive_bayes_cf(user_id):
    ratings = pd.read_csv(
        r'C:\Users\Bilal\Desktop\RS assignment\ml-latest-small\ratings.csv')
    movies = pd.read_csv(
        r'C:\Users\Bilal\Desktop\RS assignment\ml-latest-small\movies.csv')

    merged_data = pd.merge(ratings, movies, on='movieId')

    movie_ratings = merged_data.groupby(
        'movieId')['rating'].mean().reset_index()

    discretizer = KBinsDiscretizer(
        n_bins=5, encode='ordinal', strategy='uniform')
    merged_data['rating_bin'] = discretizer.fit_transform(
        merged_data['rating'].values.reshape(-1, 1))

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(merged_data['title'])

    naive_bayes = MultinomialNB()
    naive_bayes.fit(X, merged_data['rating_bin'])

    def recommend_movies(user_input, top_n=5):
        user_input_vector = vectorizer.transform([user_input])
        predicted_rating_bins = naive_bayes.predict(user_input_vector)
        top_movies = merged_data.loc[merged_data['rating_bin'].isin(predicted_rating_bins)].groupby(
            'movieId')['rating'].mean().reset_index().sort_values('rating', ascending=False).head(top_n)
        recommended_movies = pd.merge(top_movies, movies, on='movieId')
        return recommended_movies[['title', 'rating']]

    user_input = user_id
    recommended_movies = recommend_movies(user_input, top_n=5)

    titles_list = recommended_movies['title'].tolist()
    return titles_list
