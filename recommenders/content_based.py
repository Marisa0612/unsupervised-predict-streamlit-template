"""

    Content-based filtering for item recommendation.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: You are required to extend this baseline algorithm to enable more
    efficient and accurate computation of recommendations.

    !! You must not change the name and signature (arguments) of the
    prediction function, `content_model` !!

    You must however change its contents (i.e. add your own content-based
    filtering algorithm), as well as altering/adding any other functions
    as part of your improvement.

    ---------------------------------------------------------------------

    Description: Provided within this file is a baseline content-based
    filtering algorithm for rating predictions on Movie data.

"""

# Script dependencies
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Importing data
movies = pd.read_csv('resources/data/movies.csv', sep = ',',delimiter=',')
ratings = pd.read_csv('resources/data/ratings.csv')
movies.dropna(inplace=True)

def data_preprocessing(df):
    """Prepare data for use within Content filtering algorithm.

    Parameters
    ----------
    subset_size : int
        Number of movies to use within the algorithm.

    Returns
    -------
    Pandas Dataframe
        Subset of movies selected for content-based filtering.

    """
    lwmovies = df.copy()
    # Split genre data into individual words.
    lwmovies['keyWords'] = lwmovies['genres'].str.replace('|', ' ')
    lwmovies['genres'] = lwmovies['genres'].apply(str).apply(lambda x: x.split('|'))
    return lwmovies

# !! DO NOT CHANGE THIS FUNCTION SIGNATURE !!
# You are, however, encouraged to change its content.  
def content_model(movie_list,top_n=10):
    """Performs Content filtering based upon a list of movies supplied
       by the app user.

    Parameters
    ----------
    movie_list : list (str)
        Favorite movies chosen by the app user.
    top_n : type
        Number of top recommendations to return to the user.

    Returns
    -------
    list (str)
        Titles of the top-n movie recommendations to the user.

    """
    #Processing data
    drmovies = data_preprocessing(movies)
    genre_list = []
    for i in movie_list:
        genre_list.append(list(drmovies[drmovies['title']==i]['genres'])[0])



    from sklearn.preprocessing import MultiLabelBinarizer
    mlb2 =  MultiLabelBinarizer()
    mlb2.fit_transform(genre_list)
    genre_list = mlb2.classes_
    drmovies = drmovies[~drmovies['title'].isin(movie_list)]
    mgen = drmovies
    for gen in genre_list:
        mgen = mgen[mgen['keyWords'].str.contains(gen)]
        if len(mgen)<=top_n:
            break

        mgen2 = mgen


    mr = ratings[ratings['movieId'].isin(mgen2['movieId'].values)][['movieId', 'rating']]
    top_movies = (mr.groupby(['movieId']).mean().reset_index()).sort_values('rating', ascending =False)[:top_n]
    return list((drmovies[drmovies['movieId'].isin(top_movies['movieId'].values)]['title']).values)
