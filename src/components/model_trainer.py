# Basic Import

from src.logger import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import logging

from dataclasses import dataclass
import sys
import os

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def create_similarity_matrix(self, new):
        try:
            cv = CountVectorizer(max_features=5000, stop_words='english')
            vector = cv.fit_transform(new['tags']).toarray()
            similarity = cosine_similarity(vector)
            return similarity
        except Exception as e:
            logging.error(f"Error in create_similarity_matrix: {e}")
            return []

    def recommend(self, movie, new, similarity):
        try:
            index = new[new['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])
            recommended_movies = []
            for i in distances[1:6]:
                recommended_movies.append(new.iloc[i[0]].title)
            return recommended_movies
        except Exception as e:
            logging.error(f"Error in recommend: {e}")
            return []

    def save_model(self, new, similarity):
        try:
            pickle.dump(new, open('movie_list.pkl','wb'))
            pickle.dump(similarity, open('similarity.pkl', 'wb'))
        except Exception as e:
            logging.error(f"Error in save_model: {e}")

