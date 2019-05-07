import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming 

##### Collaborative Filtering using USER TO USER SIMILARITY:


# Let's now write a function to compute k nearest neighbours of an arbitrary active user using hamming distance. This will be the K number of closest people who are similar to this active user; we can use their highest rated viewed movies to recommend to the "Active User. We will be using the hamming distance to find distances between users.


def nearestneighbours(user_id, userItemRatingMatrix, K):
    '''This helper function finds the K nearest neighbors to a specific user using hamming distance and a useritemrating matrix. A user is closest to another if they have reviewed the same rating to the most number of items.
    
    Hamming Distance is just a binary difference between two users. If we both rate 10 books, if all ratings are exactly the same, hamming distance = 0. If we have a 3 different ratings out of 10 and 7 out of 10 ratings are exactly the same, then hamming distance = 3.'''

    # create a user df that contains all users except active user (we want to remove the active user so we don't recommend your own things to yourself)
    allUsers = pd.DataFrame(userItemRatingMatrix.index)
    allUsers = allUsers[allUsers.user_id != user_id]
    
    # Add a column to this df which contains distance of active user to each user
    allUsers["distance"] = allUsers["user_id"].apply(lambda x: hamming(userItemRatingMatrix.loc[user_id], userItemRatingMatrix.loc[x]))
    # print(allUsers.sort_values(["distance"],ascending=True).head()) # debug
    
    # sort the values of all users based on the distance metric, and will return the top K user ids - we want the closest number of users
    KnearestUsers = allUsers.sort_values(["distance"],ascending=True)["user_id"][:K]

    return KnearestUsers




def get_ratings(user_id, userItemRatingMatrix):
    '''given a user_ID, and a userItemRatingMatrix, it returns the top N number of movie recommendations by movie_id. This function uses K Nearest Users with Hamming Distance.
    
    NOW WE KNOW WHAT THE NEAREST NEIGHBORS ARE, WE WANT TO SEE WHAT THEY READ AND AVERAGE THEIR RATINGS TO FILL OUT THE MISSING RATINGS THAT WE HAVE FOR OUR USER.'''
    
    # find the 10 neighbors nearest to that user using the above helper function
    KnearestUsers = nearestneighbours(user_id, userItemRatingMatrix, 10)
    
    # get the ratings given by nearest neighbours. Note the userItemRatingMatrix index is the user_id
    NNRatings = userItemRatingMatrix[userItemRatingMatrix.index.isin(KnearestUsers)]
    
    # Find the average rating of each movie rated by ONLY the nearest neighbours.
        # np.nanmean - Computes the arithmetic mean along the specified axis, ignoring NaNs.
        # then, we're dropping movies that don't have ratings / dropping na's
    avgRating = NNRatings.apply(np.nanmean).dropna()

    # we are returning the average rating of all movies that he did not see using Collaborative Filtering using USER TO USER SIMILARITY. This is not sorted yet.
    return avgRating

    