from flask import jsonify
from google.cloud import bigquery

# Common Imports:
import pandas as pd
import numpy as np
import os
import json

# custom imports:
import query_data
import recommend_engine



#### QUERY OUR TRANSACTION AND MOVIE DATA FROM GOOGLE BIG QUERY:

# AUTHENTIFICATION:
path = os.getcwd()
path += '\classicmovies-5e206ef6ea35.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
client = bigquery.Client()

# GET DATA ----- this will query our data from the database once only when the app is loaded.
movie_dicts = query_data.get_movie(client)


# print(jsonify(movie_dicts['30s']))
print(json.dumps(movie_dicts['30s'], indent=4, sort_keys=True))
