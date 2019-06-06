import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming 



##### Collaborative Filtering using USER TO USER SIMILARITY -->>>>>>>>>>>>>

## HELPER FUNCTION - find user nearest neighbors
def unearestneighbours(user_id, userItemRatingMatrix, K):
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


## MAIN FUNCTION - fills an array of predicted ratings
def user_to_user_recommendations(user_id, userItemRatingMatrix, k=10, n=100):
    '''given a user_ID, a userItemRatingMatrix, k number of nearest neighbors, and n number of movies returned - it returns a sorted array of predicted ratings of the rest of the movies that can be used to deduce recommendations. This function uses helper function unearestneighbors with Hamming Distance.
    '''
    
    # find the N neighbors nearest to that user using the above helper function
    KnearestUsers = unearestneighbours(user_id, userItemRatingMatrix, k)
    
    # get the ratings given by nearest neighbours. Note the userItemRatingMatrix index is the user_id
    NNRatings = userItemRatingMatrix[userItemRatingMatrix.index.isin(KnearestUsers)]
    
    # Find the average rating of each movie rated by ONLY the nearest neighbours.
        # np.nanmean - Computes the arithmetic mean along the specified axis, ignoring NaNs.
        # then, we're dropping movies that don't have ratings / dropping na's
    avgRating = NNRatings.apply(np.nanmean).dropna()

    # drop the movies already seen by active user
    moviesAlreadyWatched = userItemRatingMatrix.loc[user_id].dropna().index
    avgRating = avgRating[~avgRating.index.isin(moviesAlreadyWatched)]

    # index is movie_id, [:N] is for the top movie_ids sorted by avgRating.
    topMovies = avgRating.sort_values(ascending=False).index[:n]

    # we are returning the average rating of all the other movies that the user did not choose - This is not sorted yet.
    return list(topMovies)




#### ITEM TO ITEM RECOMMENDATION ->>>>>>>>>>>>>>>>>>>>>>>

##--------HELPER FUNCTION: FIND NEAREST ITEM NEIGHBOURS
def inearestneighbours(movie_id, k, userItemRatingMatrix, distance_measure = hamming):
    '''This helper function finds the K nearest neighbor item to a specific user's item using a selected distance measure.''' 

    # create a movie df that contains all movies except the selected movie input
    allMovies = pd.DataFrame(userItemRatingMatrix.index)
    # allMovies = allMovies[allMovies.movie_id != movie_id]
    
    # Add a column to this df which contains distance of active movie to each and every movie
    allMovies["distance"] = allMovies["movie_id"].apply(lambda x: distance_measure(userItemRatingMatrix.loc[movie_id], userItemRatingMatrix.loc[x]))
    
    # sort the values of all movies based on the distance metric
    sortedMovies = allMovies.sort_values(["distance"],ascending=True)["movie_id"][:k]
    return list(sortedMovies)


## -- HELPER FUNCTION TO REMOVE DUPLICATES WHILE PRESERVING ORDER:
# Source: https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


##------ MAIN FUNCTION TO GET ITEM TO ITEM RECOMMENDATIONS
def item_to_item_recommendations(movie_ids, userItemRatingMatrix):
    '''This function requires a list of 4 favourite movie ids as well as the userItemRatingMatrix. It makes use of the helper function nearestneighbours that finds the K nearest neighbor items of each movie. These items are added to a recommendation list and a ranked recommendation list is returned''' 

    # transposing so the index is the movie_id 
    userItemRatingMatrix = userItemRatingMatrix.transpose()
    
    # Loop through my favourites list and use movie_id as inputs into nearestneighbours function. 
    # Create empty list of recommendation
    # Append the function's output (sortedMovies) to the recommendations list

    recommendations = []
    for movie_id in movie_ids:
        # getting 25 nearest neighbors of each movie
        sortedMovies = inearestneighbours(movie_id, 25, userItemRatingMatrix, distance_measure = hamming) 
        recommendations.append(sortedMovies)
    
    # combine 4 lists together whilst keeping order:
    combined_sorted = []
    for a, b, c, d in zip(recommendations[0], recommendations[1], recommendations[2], recommendations[3]):
        combined_sorted += [a, b, c, d]

    # removing duplicates while preserving order:
    combined_sorted = f7(combined_sorted)

    return combined_sorted





###### MAIN FUNCTION that weights all the above functions ->
def main_recommend(user_choices, userItemRatingMatrix):
    '''This function accepts the 4 choices from the active user and the userItemRatingMatrix from the transaction data and will call the other recommendation engine functions, weight them together, and return the top 10 recommended movies.'''

    # creating our active user profile with userID = 0 and appending to the userItemRatingMatrix with his/her choices and a rating of 5.0 for the choice
    for choice in user_choices:
        userItemRatingMatrix.loc[0, choice] = 5.0 # userID = 0, movie_id of choice by the user = rating of 5.0
    userItemRatingMatrix = userItemRatingMatrix.sort_index() # sorting by index to put user 0 at top

    utou_movies = user_to_user_recommendations(0, userItemRatingMatrix) # this will return top 100 movie recommendations
    itoi_movies = item_to_item_recommendations(user_choices, userItemRatingMatrix) # this will return ~100 movie recommendations based on 33 closest to each movie

    final = []

    # looping through item to item and keeping the ones that are in both lists
    for movie in itoi_movies:
        if movie in utou_movies:
            final += movie

    # we want to make sure the final list is at least 10
    for movie in itoi_movies:
        if len(final) >= 10:
                break
        elif movie not in final:
            final += movie
    
    # return no more than 10
    return final[:10]