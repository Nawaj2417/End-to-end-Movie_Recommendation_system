
from dataclasses import dataclass
import pandas as pd
import numpy as np
import ast
import os
from src.logger import logging

from src.utils import save_object


## Data Transformation config

@dataclass
class DataTransformationconfig:  
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')



## Data Ingestionconfig class

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationconfig()

    def convert(self, text):
        try:
            L = []
            for i in ast.literal_eval(text):
                L.append(i['name'])
            return L
        except Exception as e:
            logging.error(f"Error in convert: {e}")
            return []

    def convert3(self, text):
        try:
            L = []
            counter =0
            for i in  ast.literal_eval(text):
                if counter <3 :
                    L.append(i['name'])
                counter+=1
            return L
        except Exception as e:
            logging.error(f"Error in convert3: {e}")
            return []

    def fetch_director(self, text):
        try:
            L = []
            for i in ast.literal_eval(text):
                if i['job'] == 'Director':
                    L.append(i['name'])
            return L 
        except Exception as e:
            logging.error(f"Error in fetch_director: {e}")
            return []

    def collapse(self, L):
        try:
            L1 = []
            for i in L :
                L1.append(i.replace(" ", ""))
            return L1
        except Exception as e:
            logging.error(f"Error in collapse: {e}")
            return []

    def transform_data(self, df):
        try:
            df['genres'] = df['genres'].apply(self.convert)
            df['keywords'] = df['keywords'].apply(self.convert)
            df['cast'] = df['cast'].apply(self.convert)
            df['cast'] = df['cast'].apply(lambda x:x[0:3])
            df['crew'] = df['crew'].apply(self.fetch_director)
            df['overview'] = df['overview'].apply(lambda x:x.split())
            df['cast'] = df['cast'].apply(self.collapse)
            df['crew'] = df['crew'].apply(self.collapse)
            df['genres'] = df['genres'].apply(self.collapse)
            df['keywords'] = df['keywords'].apply(self.collapse)
            df['tags'] = df['overview']+ df['genres']+ df['keywords']+ df['cast']+ df['crew']
            return df
        except Exception as e:
            logging.error(f"Error in transform_data: {e}")
            return pd.DataFrame()

    def initiate_data_transformation(self, data_path):
        try:
            # Reading data
            df = pd.read_csv(data_path)

            logging.info('Read data completed')
            logging.info(f'Dataframe Head : \n{df.head().to_string()}')

            logging.info('Applying data transformations')

            # Apply the transformations
            transformed_df = self.transform_data(df)

            logging.info("Applied data transformations.")

            # Save the transformed data
            transformed_df.to_csv('transformed_data.csv', index=False)

            logging.info('Transformed data saved')

            return transformed_df
        
        except Exception as e:
            logging.error("Exception occurred in the initiate_data_transformation")
            raise e
