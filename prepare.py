#Import Libraries
import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import TimeSeriesSplit
from datetime import timedelta, datetime
from sklearn.model_selection import TimeSeriesSplit
from datetime import timedelta, datetime


# ACQUIRE
from env import host, user, password

from acquire import get_store_data


def prep_sales_data(df):
    '''This function prepares the sales data'''
        
    sales_df.sale_date = pd.to_datetime(sales_df.sale_date, infer_datetime_format=True)
    df = sales_df.set_index('sale_date')
    df['month'] = sales_df.index.month
    df['day_of_week'] = sales_df.index.day_of_week
    df['sales_total'] = sales_df.sale_amount * sales_df.item_price

    return df


def split_store_data(df):
    '''
    This function takes a DataFrame as input and splits it into training, validation, and test sets.
    The split ratio used is 80% for training, 10% for validation, and 10% for testing.
    It returns three DataFrames: train, validate, and test.
    '''
    # Convert the 'sale_date' column to datetime format
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    
    # Sort the DataFrame by the 'sale_date' column
    df = df.sort_values('sale_date')
    
    # Calculate the sizes for each split
    train_size = 0.8
    validate_size = 0.1
    test_size = 0.1
    total_size = df.shape[0]
    
    train_end_index = round(total_size * train_size)
    validate_end_index = round(total_size * (train_size + validate_size))
    
    # Split the DataFrame into train, validate, and test sets
    train = df[:train_end_index]
    validate = df[train_end_index:validate_end_index]
    test = df[validate_end_index:]
    
    return train, validate, test

def plot_column(df, column, title=None, xlabel=None, ylabel=None):
    """
    Plots a column in a DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the column to plot.
        column (str): The name of the column to plot.
        title (str): The title of the plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
    """

    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")

    if title:
        plt.title(title)

    plt.plot(df[column])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def main():
    # Load data using your acquire function
    df = get_store_data()
    
    # Prepare data
    df = prep_sales_data(df)
    
    # Split data
    train, validate, test = split_store_data(df)
    
    # Plot some columns
    plot_column(train, 'sale_amount', title='Sales Amount Over Time', xlabel='Date', ylabel='Sale Amount')
    plot_column(train, 'item_price', title='Item Price Over Time', xlabel='Date', ylabel='Item Price')

if __name__ == "__main__":
    main()


def convert_to_datetime(df):
    df.sale_date = pd.to_datetime(df.sale_date, infer_datetime_format=True)
    return df
