# set the environment variable / authentification for biguqery:
import os
path = os.getcwd()
path += '\classicmovies-5e206ef6ea35.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path


from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
my_query = '''
SELECT movie_title FROM `classicmovies.classicmovies.movies` WHERE Action = 1;
'''

QUERY = (my_query)
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.movie_title)
