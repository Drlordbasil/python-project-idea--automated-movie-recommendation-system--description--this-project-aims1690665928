import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movie_data_file):
        self.movies = pd.read_csv(movie_data_file)
        self.count_vectorizer = CountVectorizer(stop_words='english')
        self.count_matrix = self.count_vectorizer.fit_transform(
            self.movies['plot'])
        self.cosine_similarities = cosine_similarity(
            self.count_matrix, self.count_matrix)

    def find_movie_index(self, movie_title):
        movie_indices = self.movies.loc[self.movies['title'].str.lower(
        ) == movie_title.lower()].index
        return movie_indices[0] if movie_indices else -1

    def find_similar_movies(self, query_movie, num_recommended_movies=5):
        query_index = self.find_movie_index(query_movie)
        if query_index == -1:
            return "Movie not found in the dataset."

        sim_scores = list(enumerate(self.cosine_similarities[query_index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        top_movies = [self.movies.iloc[sim_score[0]]['title']
                      for sim_score in sim_scores[1: min(num_recommended_movies + 1, len(sim_scores))]]

        return top_movies


if __name__ == "__main__":
    movie_data_file = "path_to_movie_data.csv"
    query_movie = "Avatar"
    movie_recommender = MovieRecommender(movie_data_file)
    recommendations = movie_recommender.find_similar_movies(
        query_movie, num_recommended_movies=5)
    print(f"Top 5 recommended movies for '{query_movie}':")
    for movie in recommendations:
        print(movie)
