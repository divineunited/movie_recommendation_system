from flask import Flask, render_template, request
from flask import redirect, url_for
import pandas as pd
import numpy as np
import os

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


# when the form press submit, it links it to the redirect which will be sent here and then passes the variable to the result page:
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

        print(_features) # flag
        print(_features.values()) # flag

        # get the values and turn it into a list
        _features=list(_features.values())
        return redirect(url_for('result', prediction = _features, _anchor='services'))

# Wanted to redirect so that it can pass the anchor of where I want to land in the results page.
# Thank you to this code to help pass the redirect variable to this result route: 
# https://stackoverflow.com/questions/26954122/how-can-i-pass-arguments-into-redirecturl-for-of-flask
@app.route('/result/<prediction>')
def result(prediction):
    # passing the string of our prediction to our template
    return render_template("result.html", prediction = prediction)

if __name__ == "__main__":
    app.run(debug=True)