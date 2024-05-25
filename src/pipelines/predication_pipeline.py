import sys
import os
import pandas as pd
import pickle
import logging

class PredictPipeline:
    def __init__(self):
        pass

    def load_data(self):
        try:
            movie_list_path = os.path.join('artifacts', 'movie_list.pkl')
            similarity_matrix_path = os.path.join('artifacts', 'similarity.pkl')

            movie_list = pickle.load(open(movie_list_path, 'rb'))
            similarity_matrix = pickle.load(open(similarity_matrix_path, 'rb'))

            return movie_list, similarity_matrix

        except Exception as e:
            logging.error("Exception occurred in loading data")
            raise e

    def recommend(self, movie_title):
        try:
            movie_list, similarity_matrix = self.load_data()

            # Ensure the movie title exists in the data
            if movie_title not in movie_list['title'].values:
                return "Movie title not found in the data."

            index = movie_list[movie_list['title'] == movie_title].index[0]
            distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
            recommended_movies = []
            for i in distances[1:6]:
                recommended_movies.append(movie_list.iloc[i[0]].title)
            return recommended_movies

        except Exception as e:
            logging.error(f"Error in recommend: {e}")
            return []

class CustomMovie:
    def __init__(self, title:str):
        self.title = title

    def get_title(self):
        return self.title
