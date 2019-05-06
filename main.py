import pandas as pd
import numpy as np
import os

# importing different recommendation systems that we created:
import collab_UserToUser



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





##### Creating User-Item Rating Matrix with Pivot Table:

userItemRatingMatrix=pd.pivot_table(data, values='rating',
                                    index=['user_id'], columns=['movie_id'])








#### Collecting rating matrix of all movies based on a User using different systems
# then removing ALL the movies the user has ALREADY seen 
# then averaging them out across all recommendation systems, while ignoring NAN 
# then sorting them to return to user the top N. 

R1 = collab_UserToUser.get_ratings(523, userItemRatingMatrix)

print(R1)