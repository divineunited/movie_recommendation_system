import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from numpy.linalg import norm

#### ---- COLLABORATIVE USER-USER RECOMMENDATION SYSTEM USING LATENT FACTOR ANALYSIS  ----- #####

# There are many latent features in the user's rating matrix. There are many known and unknown things from a rating matrix for a specific user (R) - we can use a rating matrix and factorize that into two matrices (P and Q) and fill in the features using stochastic gradient descent. After that, we can then multiply those two matrices full of features together to get a predicted user-item rating matrix and recommend / predict the highest rated movies that the user has not seen.



def error(R,P,Q,reg=0.02):
    '''This helper function will return the error between the actual rating and the ratings calculated from P and Q matrices. It is calculating the ERROR as we run the Stochastic Gradient Descent. 
    
    inputs are R P Q which are the matrices and the output is the sum of the errors. The regularization parameter is the LABMDA in the error formula that we are trying to calculate. R is the original created COO Matrix'''
    ratings = R.data
    rows = R.row
    cols = R.col
    e = 0 
    # go through every rating (for user/item in the range)
    for ui in range(len(ratings)):
        # Save the rating, user code and movie code
        rui=ratings[ui]
        u = rows[ui]
        i = cols[ui]
        # if the rating exists (can only rate between 1 and 5), then calculate the error using the formula
        if rui>0:
            # Find the sum of errors using a dot product (np matrix multiplication)
            e= e + pow(rui-np.dot(P[u,:],Q[:,i]),2)+\
                reg*(pow(norm(P[u,:]),2)+pow(norm(Q[:,i]),2))
    return e



def create_lfa_matrix(data, userItemRatingMatrix, K=4, reg=0.02, steps=20, lrate=0.001):
    '''This function for Latent Factor Analysis needs all the transaction data (not just the useritemratingMatrix) and makes a copy of that to then create a sparse COO matrix (R) in which it will then run stoachstic gradient descent to create features P and Q. It then takes those two features, and multiplies them to come up with our final rating matrix (R2). It then takes the pivot table to add userID (index) and movieID (columns) labels to our R2. Then, uses the UserID to send back the predicted ratings for that userID.
    
    Other Parameters are K (number of features for our P and Q matrices), regularization parameter for our stochastic gradient descent (SGD), steps it takes before SGD finishes, and a learning rate for our SGD.'''
    
    # make a copy of our data before modifying it:
    data_lfa = data.copy()

    # need to change the user and books to categorical data.
    data_lfa['user_id'] = data_lfa['user_id'].astype("category")
    data_lfa['movie_id'] = data_lfa['movie_id'].astype("category")

    # then, create the COO Matrix using those categories. It creates plot points on the original matrix for user_id and movie_id that point to the specific rating value. It is created in order to store the useritemrating matrix in smaller memory - to store a sparse matrix efficiently. 
    # rows are user_id
    # columnes are movie_id
    # it assigns categorical codes in ascending order to the user and movie IDs
    R = coo_matrix((data_lfa['rating'].astype(float),
                        (data_lfa['user_id'].cat.codes,
                            data_lfa['movie_id'].cat.codes)))

    
    # Setup the dimensions using the shape of R
    # M - No. of users
    # N - No. of items
    # K - No. of features (F1, F2, F3, F4)
    # Intialise and Fill the P and Q Factor Matrices with random numbers
    M, N = R.shape
    P = np.random.rand(M,K)
    Q = np.random.rand(K,N)

    # calculate the initial RMSE with the help of our error function above:
    rmse = np.sqrt(error(R,P,Q,reg)/len(R.data))
    print("Initial RMSE: " + str(rmse))

    # complete the specified number of steps for gradient descent or if you reach a particular RMSE of less than 0.5. Feel free to change it here. Here it's ok with a rating error of 0.5. Remember RMSE is in the units of the problem. A rating error within 0.5 is acceptable.
    for step in range(steps):
        # for user and item for every rating
        for ui in range(len(R.data)):
            rui=R.data[ui] # rating for that user / item
            u = R.row[ui] # user
            i = R.col[ui] # item
            if rui>0: # if there is a rating. 
                # update P, Q in the direction of local minima
                eui=rui-np.dot(P[u,:],Q[:,i]) # error in that specific user/item = actual specific rating - the calculated (initially random) P and Q values located at that specific coordinate.
                # updating P and Q using partial derivatives - this is where the magic happens:
                P[u,:]=P[u,:]+lrate*2*(eui*Q[:,i]-reg*P[u,:])
                Q[:,i]=Q[:,i]+lrate*2*(eui*P[u,:]-reg*Q[:,i])
                
        # calculating a new RMSE after updating P and Q.
        rmse = np.sqrt(error(R,P,Q,reg)/len(R.data))
        if rmse<0.5:
            break

    print("Final RMSE: "+ str(rmse))

    # creating our new rating matrix based off our calculated P and Q fully filled features:
    R2 = np.dot(P, Q)

    # now, we can turn this into a dataframe using the previous userItemRatingMatrix index and columns to fill in the indices (user_ids) and columns (movie_ids)
    pred_matrix = pd.DataFrame(data=R2,
                index=userItemRatingMatrix.index,    
                columns=userItemRatingMatrix.columns)
    
    return pred_matrix



def get_ratings(user_id):
    '''This only needs the user_id and uses an already created Latent Factor Analysis prediction matrix to return the predicted ratings for that user. It has not removed the movies that the user already has seen, and is not sorted.'''
    pred_matrix = pd.read_csv('./data/lfa_pred_matrix.csv', index_col=0)
    return pred_matrix.loc[user_id]



##### UNCOMMENT ALL THIS TO CREATE A NEW LATENT FACTOR ANALYSIS PREDICTION MATRIX:
# # -----------------------------------------------------------------
# ##### Importing data that will be used to create recommendations:

# dataFile='./data/ml-100k/u.data'
# data = pd.read_csv(dataFile, sep="\t", header=0, names=["user_id","movie_id","rating", "timestamp"])

# movieFile='./data/ml-100k/u.item'
# movies = pd.read_csv(movieFile, sep="|", encoding='Latin-1', header=0, names=['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'Unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])


# ##### Data Cleaning:

# # only retain values from movie-rating that actually have movie meta data
# data = data[data["movie_id"].isin(movies.movie_id)]

# # only keep movies which have been rated by more than 10 users
# UsersPerMovie = data.movie_id.value_counts()
# condition = data['movie_id'].isin(UsersPerMovie[UsersPerMovie > 10].index)
# data = data[condition]

# # Now, we have our user-item rating matrix. We have 943 users and 1,118 movies. We started off with 1,682 movies, but we whittled down the movie list to 1,118 by removing movies that had less than 10 reviews.



# ##### Creating User-Item Rating Matrix with Pivot Table:
# userItemRatingMatrix=pd.pivot_table(data, values='rating',
#                                     index=['user_id'], columns=['movie_id'])


##### Creating our LFA Prediction Matrix for future Use:
# pred_matrix = create_lfa_matrix(data, userItemRatingMatrix)
# pred_matrix.to_csv(path_or_buf="data/lfa_pred_matrix.csv")
''' NOTE:
Initial RMSE: 2.8400367832677835
Final RMSE: 0.9917569189307901
'''

# # -----------------------------------------------------------------




