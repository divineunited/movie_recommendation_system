import pandas as pd
import numpy as np
import os


def cosine_user(n,m): #n is the person's ID, m is the top m similar users returned

    allUsers = userItemRatingMatrix.values
    user1 = allUsers[n] 
    denominator1 = np.sqrt(sum([np.square(x) for x in user1]))

    cosinesimilarity = [(n,1)]

    i = 1

    for user in allUsers[1:]:
        numerator = [x*y for x,y in zip(user1,user)]
        denominator2 = np.sqrt(sum([np.square(x) for x in user]))
        costheta = sum(numerator) / (denominator1 * denominator2)
        cosinesimilarity.append((userItemRatingMatrix.index[i], costheta))
        i += 1
    
    #cosinesimilarity.sort(key = lambda x:x[1], reverse = True)
    #similar_m_users = cosinesimilarity[0:m] 
    
    #create a dataframe to store the top m similar person
 
    topmusersdf = pd.DataFrame()

    for user in cosinesimilarity:
        topmusersdf = topmusersdf.append(userItemRatingMatrix.loc[user[0]])

    topmusersdf['costheta'] = [user[1] for user in cosinesimilarity]

    all_values_1 = topmusersdf.values

    denominator = sum([x[1] for x in cosinesimilarity])

    inx = 0
    values = []
    for x in topmusersdf.loc[n]:
        totalsum = 0
        if x == 0.0:
            for v in range(1,10):
             totalsum += all_values_1[v-1][inx] * all_values_1[v-1][1118]
        topmusersdf.loc[n][inx+1] = totalsum / denominator
    inx += 1
  
    return topmusersdf.iloc[n-1:n,:]




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


print(cosine_user(6))


