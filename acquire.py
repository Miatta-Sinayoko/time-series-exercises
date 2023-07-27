import pandas as pd
import numpy as np
import os
import math
import matplotlib as plt
import seaborn as sns

import datetime
import requests
from io import StringIO



#ACQUIRE
from env import host, user, password

def get_connection(db_name, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'

def get_store_data():
    '''
    This function reads in the store, sales, and item data from the database
    and returns a pandas DataFrame with all columns.
    If the data exists in a CSV file, it reads the data from the file.
    If the data is not available in the CSV file, it reads it from the database.
    '''

    filename = 'tsa_store.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=0)
    else:
        # Replace the following SQL query with the appropriate SQL code to retrieve data from the database.
        # For the purpose of this example, we'll use a placeholder query.
        sql = '''
        SELECT *
        FROM sales
        JOIN items USING (item_id)
        JOIN stores USING (store_id)
        LIMIT 10000;
        '''
        
        # Replace 'get_connection()' with the appropriate function that returns the database connection.
        # For the purpose of this example, we'll use a placeholder function.
        df = pd.read_sql(sql, get_connection('tsa_item_demand'))

        # Save the data to a CSV file for future use.
        df.to_csv(filename, index=False)

        return df



def get_swapi_data(url):
    data = []
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            results = json_data['results']
            data.extend(results)
            url = json_data['next']
            if url is None:
                break
        else:
            print(f"Error: {response.status_code}")
            break
    return pd.DataFrame(data)
 
def get_starwars_data(starwars_df):
    '''This function creates a csv for concat time_series csv'''
    # Assuming you have a function 'get_starwars_data()' that retrieves the starwars data and returns a DataFrame
    df_starwars = starwars_df

    # Save the DataFrame to a CSV file
    df_starwars.to_csv("starwars.csv", index=False)  # Specify 'index=False' to exclude the index column in the CSV

    filename = 'time_series.csv'
    if os.path.isfile(filename):
        
        return pd.read_csv(filename)
# get_starwars_data(starwars_df)

def get_power_data():
    '''
    This function acquires the Open Power Systems Data for Germany.
    It first checks if the data file exists locally and reads it if available.
    If the file doesn't exist, it will download the data and save it as a CSV file.
    Returns a pandas DataFrame with all columns.
    '''
    filename = 'opsd_germany_daily.csv'

    # Verify if file exists
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    # Download data if file doesn't exist
    else:
        url = "https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for any download errors
            data = response.text
            df = pd.read_csv(StringIO(data))
            df.to_csv(filename, index=False)
            print("Data acquired and saved successfully.")
            return df
        except Exception as e:
            print("Error acquiring data:", e)
            return None

# Example usage:
if __name__ == "__main__":
    power_data_df = get_power_data()
    if power_data_df is not None:
        print(power_data_df.head())


