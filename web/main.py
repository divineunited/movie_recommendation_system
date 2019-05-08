from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os

# service section HTML found here:
import service

app=Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home(service):
    if request.method == 'GET':
        html = 'html = service.get_index()'
        # renders the text for the service section of our webpage depending on if it's a GET or POST request
        return render_template("index.html", service = html)
    else:
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
        
        # passing the string of our prediction to our template
        return render_template("index.html", _anchor="services", service=service.result)



# when the form press submit, it links it to the action /result which will be sent here:
@app.route('/result', methods = ['POST'])
def result():
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
        
        # passing the string of our prediction to our template
        return render_template("result.html", prediction=_features) 

if __name__ == "__main__":
    app.run(debug=True)