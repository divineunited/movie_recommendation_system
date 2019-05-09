import pandas as pd
import numpy as np
import os
from scipy.stats import pearsonr
import math
from math import sqrt


def similarmovies(n,method):

    if method == 'cosine':
        y = cosine_user(n)
    
    elif method == 'pearsons':
        y = pearsons_user(n)
    
    else:
        y = eucli_user(n)

    return y




def cosine_movie(n): #n is the person's ID

    allUsers = userItemRatingMatrix.values
    usern = np.array(userItemRatingMatrix.loc[n])
    denominator1 = np.sqrt(sum([np.square(x) for x in usern]))

    cosinesimilarity = []

    i = 0

    for user in allUsers[0:]:
        numerator = [x*y for x,y in zip(usern,user)]
        denominator2 = np.sqrt(sum([np.square(x) for x in user]))
        costheta = sum(numerator) / (denominator1 * denominator2)
        cosinesimilarity.append((userItemRatingMatrix.index[i], costheta))
        i += 1

    cosinesimilarity.sort(key = lambda x:x[1], reverse = True)
    similar_10_users = cosinesimilarity[1:11] 
    
 
    usersdf = pd.DataFrame()

    for user in similar_10_users:
        usersdf = usersdf.append(userItemRatingMatrix.loc[user[0]])

    usersdf['costheta'] = [user[1] for user in similar_10_users]
    
    usersdf_index = []

    for index in usersdf.index:
        usersdf_index.append(index)
    # all_values = usersdf.values

    # denominator = sum([x[1] for x in cosinesimilarity])

    # inx = 0
    
    # for x in usersdf.loc[n]:
    #     totalsum = 0
    #     if x == 0.0:
    #         for v in range(1,1118):
    #          totalsum += all_values[v-1][inx] * all_values[v-1][1117]
    #     usersdf.loc[n][inx+1] = totalsum / denominator
    #     inx += 1
    

    return usersdf_index


def pearsons_movie(n):
    allUsersdf = pd.DataFrame(userItemRatingMatrix.index)
    user = n

    allUsers = userItemRatingMatrix.values

    user1 = allUsers[0]
    Pearson_corr = allUsersdf["movie_id"].apply(lambda x: pearsonr(userItemRatingMatrix.loc[n],userItemRatingMatrix.loc[x]))
    b = [list(x) for x in Pearson_corr]
    pearsonsimilarity = []

    i = 0

    for user in allUsers[0:]:
        pearsonsimilarity.append((userItemRatingMatrix.index[i], b[i][0]))
        i += 1

    pearsonsimilarity.sort(key = lambda x:x[1], reverse = True)
    similar_10_users = pearsonsimilarity[1:11] 
    
    usersdf = pd.DataFrame()
    usersdf

    for user in similar_10_users:
        usersdf = usersdf.append(userItemRatingMatrix.loc[user[0]])

    usersdf['pearson'] = [user[1] for user in similar_10_users]

    usersdf_index = []

    for index in usersdf.index:
        usersdf_index.append(index)

    # all_values = usersdf.values

    # denominator = sum([x[1] for x in pearsonsimilarity])

    # inx = 0
    
    # for x in usersdf.loc[n]:
    #     totalsum = 0
    #     if x == 0.0:
    #         for v in range(1,942):
    #          totalsum += all_values[v-1][inx] * all_values[v-1][941]
    #     usersdf.loc[n][inx+1] = totalsum / denominator
    #     inx += 1
    

    return usersdf_index

def eucli_movie(n):
    allUsersdf = pd.DataFrame(userItemRatingMatrix.index)
    user = n

    allUsers = userItemRatingMatrix.values

    user1 = allUsers[0]
    
    euclisimilarity = []

    i = 0
    pn = [score for key, score in userItemRatingMatrix.loc[n].items()]

    for user in userItemRatingMatrix.index:
 
        pm = [score for key, score in userItemRatingMatrix.loc[user].items()]
        sum_of_square = sum(pow(pn[index]-pm[index],2) for index in range(len(pn)) if pm[index] != 0 and pn[index] != 0)
        euclicorr = 1/(1+sum_of_square)
        euclisimilarity.append((userItemRatingMatrix.index[i], euclicorr))
        i += 1

    euclisimilarity.sort(key = lambda x:x[1], reverse = True)
    similar_10_users = euclisimilarity[1:11] 


    usersdf = pd.DataFrame()
    usersdf

    for user in similar_10_users :
        usersdf = usersdf.append(userItemRatingMatrix.loc[user[0]])
    usersdf['eucli'] = [user[1] for user in similar_10_users ]

    usersdf_index = []

    for index in usersdf.index:
        usersdf_index.append(index)

    # all_values = usersdf.values

    # denominator = sum([x[1] for x in euclisimilarity])

    # inx = 0
    
    # for x in usersdf.loc[n]:
    #     totalsum = 0
    #     if x == 0.0:
    #         for v in range(1,942):
    #          totalsum += all_values[v-1][inx] * all_values[v-1][941]
    #     usersdf.loc[n][inx+1] = totalsum / denominator
    #     inx += 1
    
    return usersdf_index

def your_item_to_item_recommendations(my_favourites_list):
    '''This function requires the user to input a list of favourite movie ids. It makes use of the helper function nearestneighbours that finds the K nearest neighbor items of each movie. These items are added to a recommendation list and a ranked recommendation list is returned''' 

    
    #Loop through my favourites list and use movie_id as inputs into nearestneighbours function. 
    #Create empty list of recommendation
    #Append the function's output (sortedMovies) to the recommendations list

    for i in range(0, len(my_favourites_list)):
        my_favourites_list[i]= int(my_favourites_list[i])

    recommendations= []
    for movie_id in my_favourites_list:

        sortedMovies = eucli_movie(movie_id) 
        
    # #the output of this function isvsortedMovies
        recommendations = recommendations + sortedMovies

    #we want to sort according to the movies that appeared in all 4 recommendation list

    recommendations=sorted(recommendations,key=recommendations.count, reverse=True)

    return recommendations



#### TESTING FUNCTION BELOW:

dataFile='./data/ml-100k/u.data'
data = pd.read_csv(dataFile, sep="\t", header=0, names=["user_id","movie_id","rating", "timestamp"])

movieFile='./data/ml-100k/u.item'
movies = pd.read_csv(movieFile, sep="|", encoding='Latin-1', header=0, names=['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'Unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

data = data[data["movie_id"].isin(movies.movie_id)]

# only keep movies which have been rated by more than 10 users
UsersPerMovie = data.movie_id.value_counts()
condition = data['movie_id'].isin(UsersPerMovie[UsersPerMovie > 10].index)
data = data[condition]

##### Creating User-Item Rating Matrix with Pivot Table:

userItemRatingMatrix=pd.pivot_table(data, values='rating',
                                    index=['movie_id'], columns=['user_id']).fillna(0)


## Return the top 10 users who are most similar to user1 by consine theory


#print(eucli_user(10))
#print(eucli_user(10))  #method: 'consine', 'pearsons', if no input, return eucli_distance
myList = [10,20,30]

print(your_item_to_item_recommendations(myList))