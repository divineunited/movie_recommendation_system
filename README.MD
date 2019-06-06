# Movie Recommendation System

This full stack movie recommendation web application system is based on a MovieLens archival dataset that can be used to recommend classic movies. It utilizes both item to item recommendation and collaborative user to user recommendation algorithms based on transaction data captured in a seven month period in 1997. When the user chooses 4 movies, it registers the user as a new user utilizing those 4 choices to do both item-item recommendation + user-user recommendation. The program then weights the results and returns the top 10 recommendations. 

The data is stored on Google Big Query and is queried appropriately when the app is called. The data is serviced by a FLASK / PYTHON service layer and a BOOTSTRAP / JQUERY front-end. It is hosted using Google App Engine.

## TRY IT OUT HERE: ##
# https://classicmovies.appspot.com/



***NOTE: Since recommendations are based on the ratings of other users in 1997, some recommendations might not be age-appropriate (e.g. many users might have highly R-rated movies like Silence of the Lambs as well as PG-rated movies like Aladdin).***


**About The Data Set:**
 
This data set consists of:
	- 100,000 ratings (1-5) from 943 users on 1682 movies. 
	- Each user has rated at least 20 movies. 
    - Simple demographic info for the users (age, gender, occupation, zip)

The data was collected through the MovieLens web site
(movielens.umn.edu) during the seven-month period from September 19th, 
1997 through April 22nd, 1998. This data has been cleaned up - users
who had less than 20 ratings or did not have complete demographic
information were removed from this data set. 