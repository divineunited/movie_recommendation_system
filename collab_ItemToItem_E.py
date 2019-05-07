import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming 

##### Collaborative Filtering using ITEM TO ITEM SIMILARITY:


def nearestneighbours(movie_id, data, K):
    # This helper function finds the K nearest neighbor item to a specific user's item using hamming distance and a useritemrating matrix. 
    #Hamming Distance is just a binary difference between two items.
    # Now lets create the user-item-rating matrix
    # We create userItemRatingMatrixforItem where index is movie_id 
    userItemRatingMatrixforItem=pd.pivot_table(data, values='rating',
                                    index=['movie_id'], columns=['user_id'])


    # create a user df that contains all users except active user (we want to remove the active user so we don't recommend your own things to yourself)
    allMovies = pd.DataFrame(userItemRatingMatrixforItem.index)
    allMovies = allMovies[allMovies.movie_id != movie_id]
    
    # Add a column to this df which contains distance of active user to each user
    allMovies["distance"] = allMovies["movie_id"].apply(lambda x: hamming(userItemRatingMatrixforItem.loc[movie_id], userItemRatingMatrixforItem.loc[x]))
    # print(allMovies.sort_values(["distance"],ascending=True).head()) # debug
    
    # sort the values of all movies based on the distance metric, and will return the top K movie ids - we want the closest number of users
    KnearestMovies = allMovies.sort_values(["distance"],ascending=True)["movie_id"][:K]

    return KnearestMovies


# def get_ratings(movie_id, userItemRatingMatrixforItem):
#     '''given a user_ID, and a userItemRatingMatrix, it returns the top N number of movie recommendations by movie_id. This function uses K Nearest Users with Hamming Distance.
    
#     NOW WE KNOW WHAT THE NEAREST NEIGHBORS ARE, WE WANT TO SEE WHAT THEY READ AND AVERAGE THEIR RATINGS TO FILL OUT THE MISSING RATINGS THAT WE HAVE FOR OUR USER.'''
    
#     # find the 10 neighbor items nearest to that user's item using the above helper function
#     KnearestMovies = nearestneighbours(movie_id, userItemRatingMatrixforItem, 10)
    
#     # get the ratings of nearest items. Note the userItemRatingMatrixforItem index is the movie_id
#     NNRatings = userItemRatingMatrixforItem[userItemRatingMatrixforItem.index.isin(KnearestMovies)]
    
#     # Find the average rating of each movie rated by ONLY the nearest neighbours.
#         # np.nanmean - Computes the arithmetic mean along the specified axis, ignoring NaNs.
#         # then, we're dropping movies that don't have ratings / dropping na's
#     avgRating = NNRatings.apply(np.nanmean).dropna()
    
#     # drop the movies already seen by active user
#     #moviesAlreadyWatched = userItemRatingMatrix.loc[user_id].dropna().index
#     avgRating = avgRating[~avgRating.index.isin(moviesAlreadyWatched)]

#     # index is movie_id, [:N] is for the top movie_ids sorted by avgRating.
#     topMovies = avgRating.sort_values(ascending=False).index[:N]

#     # we are returning the average rating of all movies that he did not see using Collaborative Filtering using USER TO USER SIMILARITY. This is not sorted yet.
#     return avgRating

    










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

print(nearestneighbours(200, data, 10))
