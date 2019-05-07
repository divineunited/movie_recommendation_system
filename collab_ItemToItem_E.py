import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming 

##### Collaborative Filtering using ITEM TO ITEM SIMILARITY:

# KNN format is used, but we want a list with all movies sorted, not limited to K.

def nearestneighbours(movie_id, data, distance_measure = hamming):
    '''This helper function finds the K nearest neighbor item to a specific user's item using a selected distance measure.''' 
    
    # We create userItemRatingMatrixforItem where index is movie_id 
    userItemRatingMatrixforItem=pd.pivot_table(data, values='rating',
                                    index=['movie_id'], columns=['user_id'])


    # create a movie df that contains all movies except the selected movie input
    allMovies = pd.DataFrame(userItemRatingMatrixforItem.index)
    allMovies = allMovies[allMovies.movie_id != movie_id]
    
    # Add a column to this df which contains distance of active movie to each and every movie
    allMovies["distance"] = allMovies["movie_id"].apply(lambda x: distance_measure(userItemRatingMatrixforItem.loc[movie_id], userItemRatingMatrixforItem.loc[x]))
    # print(allMovies.sort_values(["distance"],ascending=True).head()) # debug
    
    # sort the values of all movies based on the distance metric
    sortedMovies = allMovies.sort_values(["distance"],ascending=True)["movie_id"]

    return sortedMovies






#### ------------ FUNCTION TESTING:

##### Importing data that will be used to create recommendations:

dataFile='./data/ml-100k/u.data'
data = pd.read_csv(dataFile, sep="\t", header=0, names=["user_id","movie_id","rating", "timestamp"])

movieFile='./data/ml-100k/u.item'
movies = pd.read_csv(movieFile, sep="|", encoding='Latin-1', header=0, names=['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'Unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])





##### Data Cleaning:

# only retain values from movie-rating that actually have movie meta data
data = data[data["movie_id"].isin(movies.movie_id)]

# only keep movies which have been rated by more than 10 users
UsersPerMovie = data.movie_id.value_counts()
condition = data['movie_id'].isin(UsersPerMovie[UsersPerMovie > 10].index)
data = data[condition]

# Now, we have our user-item rating matrix. We have 943 users and 1,118 movies. We started off with 1,682 movies, but we whittled down the movie list to 1,118 by removing movies that had less than 10 reviews.

print(nearestneighbours(2, data))
