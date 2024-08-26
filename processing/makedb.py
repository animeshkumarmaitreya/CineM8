import os
from processing import nlp
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Main():
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self):
        self.new_df=None
        self.movies=None
        self.movies2=None

    def getter(self):
        return self.new_df, self.movies, self.movies2
    
    def get_df(self):
        pickle_file_path=r'data/new_df_dict.pkl'
        if os.path.exists(pickle_file_path):
            pickle_file_path=r'data/movies_dict.pkl'
            with open(pickle_file_path,'rb') as pickle_file:
                loaded_dict=pickle.load(pickle_file)
            self.movies=pd.DataFrame.from_dict(loaded_dict) 
            pickle_file_path=r'data/movies2_dict.pkl'
            with open(pickle_file_path, 'rb') as pickle_file:
                loaded_dict_2 = pickle.load(pickle_file)
            self.movies2 = pd.DataFrame.from_dict(loaded_dict_2)
            pickle_file_path = r'data/new_df_dict.pkl'
            with open(pickle_file_path, 'rb') as pickle_file:
                loaded_dict = pickle.load(pickle_file)
            self.new_df = pd.DataFrame.from_dict(loaded_dict)

        else:
            self.movies, self.new_df, self.movies2 = nlp.read_csv_to_df()
            movies_dict = self.movies.to_dict()

            pickle_file_path = r'data/movies_dict.pkl'
            with open(pickle_file_path, 'wb') as pickle_file:
                pickle.dump(movies_dict, pickle_file)

            movies2_dict = self.movies2.to_dict()

            pickle_file_path = r'data/movies2_dict.pkl'
            with open(pickle_file_path, 'wb') as pickle_file:
                pickle.dump(movies2_dict, pickle_file)

            df_dict = self.new_df.to_dict()

            pickle_file_path = r'data/new_df_dict.pkl'
            with open(pickle_file_path, 'wb') as pickle_file:
                pickle.dump(df_dict, pickle_file)

    def vectorise(self, col_name):
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vec_tags = cv.fit_transform(self.new_df[col_name]).toarray()
        sim_bt = cosine_similarity(vec_tags)
        return sim_bt

    def get_similarity(self, col_name):
        pickle_file_path = fr'data/similarity_tags_{col_name}.pkl'
        if os.path.exists(pickle_file_path):
            pass
        else:
            similarity_tags = self.vectorise(col_name)

            with open(pickle_file_path, 'wb') as pickle_file:
                pickle.dump(similarity_tags, pickle_file)

    def main_(self):
        self.get_df()
        self.get_similarity('tags')
        self.get_similarity('genres')
        self.get_similarity('keywords')
        self.get_similarity('tcast')
        self.get_similarity('tprduction_comp')