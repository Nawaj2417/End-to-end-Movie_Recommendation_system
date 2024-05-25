import os
import sys
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.model_trainer import ModelTrainer
from src.components.data_transformation import DataTransformation



if __name__=='__main__':
    obj = DataIngestion()
    movie_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    new = data_transformation.initiate_data_transformation(movie_data)

    model_trainer = ModelTrainer()
    model_trainer.initate_model_training(new)