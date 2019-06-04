from google.cloud import bigquery


def get_movie(client):
    '''USED TO GET MOVIE DATA FOR DROPDOWN SELECTIONS. This function requires an authenticated google bigquery client and returns an array of hashtables with year, (genre), movie_ids, and movie_titles as keys and their corresponding values from Google Big Query. It also returns a dictionary of movie_ids as keys and movie_titles as values'''

    # can get the GENRE later - need to unpivot first
    # source: unpivot of genre columns: https://stackoverflow.com/questions/16784999/sql-get-column-names-when-value-is-1
    movie_query = 'SELECT movie_id, movie_title, EXTRACT(YEAR FROM release_date) as movie_year FROM `classicmovies.classicmovies.movies` ORDER BY movie_year ASC'
    QUERY = (movie_query)
    query_job = client.query(QUERY) # API request
    rows = query_job.result() # Waits for query to finish

    # creating a Dictionary of Decades that we will populate accordingly below
    movie_dicts = {'20s':[], '30s':[], '40s':[], '50s':[], '60s':[], '70s':[], '80s':[], '90s':[]}

    for row in rows:
        movie_dict = {}
        movie_dict['movie_id'] = row.movie_id
        movie_dict['movie_title'] = row.movie_title
        movie_dict['movie_year'] = row.movie_year

        if 1920 <= row.movie_year <= 1929:
            movie_dicts['20s'].append(movie_dict)
        elif 1930 <= row.movie_year <= 1939:
            movie_dicts['30s'].append(movie_dict)
        elif 1940 <= row.movie_year <= 1949:
            movie_dicts['40s'].append(movie_dict)
        elif 1950 <= row.movie_year <= 1959:
            movie_dicts['50s'].append(movie_dict)
        elif 1960 <= row.movie_year <= 1969:
            movie_dicts['60s'].append(movie_dict)
        elif 1970 <= row.movie_year <= 1979:
            movie_dicts['70s'].append(movie_dict)
        elif 1980 <= row.movie_year <= 1989:
            movie_dicts['80s'].append(movie_dict)
        else:
            movie_dicts['90s'].append(movie_dict)

    return movie_dicts



def get_data(client):
    '''USED TO GET TRANSACTION DATA FOR RECOMMENDATION ENGINE. This function requires an authenticated google bigquery client and returns a Pandas dataframe of all transactions that our recommendation engine can use to make recommendations.'''

    my_query = 'SELECT user_id, movie_id, rating FROM `classicmovies.classicmovies.transactions`'
    QUERY = (my_query)
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    
    return rows.to_dataframe()


######### Function Testing:

# import os

# ## AUTHENTIFICATION:
# path = os.getcwd()
# path += '\classicmovies-5e206ef6ea35.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
# client = bigquery.Client()

# print(get_movie(client))
# print(get_data(client).head())