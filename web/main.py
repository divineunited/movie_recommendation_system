from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os

app=Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

# # when the form press submit, it links it to the action /result which will be sent here:
# @app.route('/result', methods = ['POST'])
# def result():
#     prediction=''
#     if request.method == 'POST':

#         prediction = 'This cell is likely INFECTED with the Malaria Parasite.'

#         print(prediction) # flag

#         # passing the string of our prediction to our template
#         return render_template("result.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)