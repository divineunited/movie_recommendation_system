import pandas as pd
import numpy as np
import os
from scipy.stats import pearsonr
import math
from math import sqrt


def cosine_user(n): #n is the person's ID

    allUsers = userItemRatingMatrix.values
    usern = allUsers[n] 
    denominator1 = np.sqrt(sum([np.square(x) for x in usern]))

    cosinesimilarity = []

    i = 0

    for user in allUsers[1:]:
        numerator = [x*y for x,y in zip(usern,user)]
        denominator2 = np.sqrt(sum([np.square(x) for x in user]))
        costheta = sum(numerator) / (denominator1 * denominator2)
        cosinesimilarity.append((userItemRatingMatrix.index[i], costheta))
        i += 1
    
 
    usersdf = pd.DataFrame()

    for user in cosinesimilarity:
        usersdf = usersdf.append(userItemRatingMatrix.loc[user[0]])

    usersdf['costheta'] = [user[1] for user in cosinesimilarity]

    all_values = usersdf.values

    denominator = sum([x[1] for x in cosinesimilarity])

    inx = 0
    
    for x in usersdf.loc[n]:
        totalsum = 0
        if x == 0.0:
            for v in range(1,942):
             totalsum += all_values[v-1][inx] * all_values[v-1][941]
        usersdf.loc[n][inx+1] = totalsum / denominator
        inx += 1
  
    return usersdf.loc[n]


def pearsons_user(n):
    allUsersdf = pd.DataFrame(userItemRatingMatrix.index)
    user = n

    allUsers = userItemRatingMatrix.values

    user1 = allUsers[0]
    Pearson_corr = allUsersdf["user_id"].apply(lambda x: pearsonr(userItemRatingMatrix.loc[n],userItemRatingMatrix.loc[x]))
    b = [list(x) for x in Pearson_corr]
    pearsonsimilarity = []

    i = 0

    for user in allUsers[0:]:
        pearsonsimilarity.append((userItemRatingMatrix.index[i], b[i][0]))
        i += 1
    
    usersdf = pd.DataFrame()
    usersdf

    for user in pearsonsimilarity:
        usersdf = usersdf.append(userItemRatingMatrix.loc[user[0]])

    usersdf['pearson'] = [user[1] for user in pearsonsimilarity]

    all_values = usersdf.values

    denominator = sum([x[1] for x in pearsonsimilarity])

    inx = 0
    
    for x in usersdf.loc[n]:
        totalsum = 0
        if x == 0.0:
            for v in range(1,942):
             totalsum += all_values[v-1][inx] * all_values[v-1][941]
        usersdf.loc[n][inx+1] = totalsum / denominator
        inx += 1
    

    return usersdf.loc[n]

def eucli_user(n):
    allUsersdf = pd.DataFrame(userItemRatingMatrix.index)
    user = n

    allUsers = userItemRatingMatrix.values

    user1 = allUsers[0]
    
    euclisimilarity = []

    i = 0
    pn = [score for key, score in result.loc[n].items()]

    for user in result.index:
 
        pm = [score for key, score in result.loc[user].items()]
        sum_of_square = sum(pow(pn[index]-pm[index],2) for index in range(len(pn)) if pm[index] != 0 and pn[index] != 0)
        euclicorr = 1/(1+sum_of_square)
        euclisimilarity.append((userItemRatingMatrix.index[i], euclicorr))
        i += 1

    usersdf = pd.DataFrame()
    usersdf

    for user in euclisimilarity:
        usersdf = usersdf.append(userItemRatingMatrix.loc[user[0]])
    usersdf['eucli'] = [user[1] for user in euclisimilarity]

    all_values = usersdf.values

    denominator = sum([x[1] for x in euclisimilarity])

    inx = 0
    
    for x in usersdf.loc[n]:
        totalsum = 0
        if x == 0.0:
            for v in range(1,942):
             totalsum += all_values[v-1][inx] * all_values[v-1][941]
        usersdf.loc[n][inx+1] = totalsum / denominator
        inx += 1
    
    return usersdf.loc[n]





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
                                    index=['user_id'], columns=['movie_id']).fillna(0)

userItemRatingMatrix1=pd.pivot_table(data, values='rating',
                                    index=['user_id'], columns=['movie_id'])
## Return the top 10 users who are most similar to user1 by consine theory


print(eucli_user(10))


