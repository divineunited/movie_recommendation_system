from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
from google.cloud import bigquery

# Common Imports:
import pandas as pd
import numpy as np
import os
import json

# custom imports:
import query_data
import recommend_engine

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True



#### QUERY OUR TRANSACTION AND MOVIE DATA FROM GOOGLE BIG QUERY:
# AUTHENTIFICATION:
path = os.getcwd()
path += '\classicmovies-5e206ef6ea35.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
client = bigquery.Client()

# GET DATA ----- this will query our data from the database once only when the app is loaded.
movie_dicts, id_movie = query_data.get_movie(client) # getting movie data in form of decades:{movie_id, movie_title, movie_year} as well as id_movie simple dictionary 
data = query_data.get_data(client) # getting dataframe of transaction data for our recommendation systems


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html", decades = list(movie_dicts.keys())) # passing the keys (decades) as a list to JS front end


# this is an API endpoint for AJAX to update our movie dropdowns based on the choice of decade. It sends the decade, and then uses the data in our server that was queried from database to send AJAX asynchronous update for dropdown.
@app.route('/get_movies/<decade>')
def get_movies(decade):
    if decade not in movie_dicts:
        return jsonify([])
    else:
        return jsonify(movie_dicts[decade])


# when the form press submit, it links it to the redirect which will be sent here and then passes the prediction variable to the results page after back-end recommendation logic completed:
@app.route('/myredirect', methods = ['POST'])
def my_redirect():
    if request.method == 'POST':
        # from the request form, convert it to a dictionary saved as this variable
        _features = request.form.to_dict()

        ### converting inputs to their correct value types:
        _features['movie_1'] = int(_features['movie_1'])
        _features['movie_2'] = int(_features['movie_2'])
        _features['movie_3'] = int(_features['movie_3'])
        _features['movie_4'] = int(_features['movie_4'])

        # get the values and turn it into a list
        _features=list(_features.values())

        # get our recommended movie_ids:
        movie_ids = recommend_engine.your_item_to_item_recommendations(_features, data)

        # convert them to movie titles:
        predictions = [id_movie[id] for id in movie_ids]

        # send it as a proper JSON dumps string for the redirect routing so that it can be unpacked using a JSON loads:
        predictions = json.dumps(predictions)

        # passing our predictions JSON dump and an achor to the result url.
        return redirect(url_for('result', predictions = predictions, _anchor='services'))



# Wanted to redirect so that it can pass the anchor of where I want to land in the results page (services subsection of page).
# Thank you to this code to help pass the redirect variable to this result route: 
# https://stackoverflow.com/questions/26954122/how-can-i-pass-arguments-into-redirecturl-for-of-flask
@app.route('/result/<predictions>')
def result(predictions):

    # taking our passed json dump and loading it back out as a list to pass to our results template
    predictions = json.loads(predictions)

    return render_template("result.html", predictions = predictions)

if __name__ == "__main__":
    app.run(debug=True)