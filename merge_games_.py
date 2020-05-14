import numpy as np
import pandas as pd
import copy

from src.merge_games import merge_game_ids

def merger(num_games):
    '''
    From the function 'nfl_stats_aggregator.py', the aggregated_2014_to_2019.csv file
    was created and stored in data/ folder.
    This csv has two rows per game, one for the home team and one for the away team.
    The function merge_game_ids merges the game into one row.

    merge_game_ids stores the csv into a file 'data/merged_games.csv' for use in
    machine learning models
    '''
    
    # pull in two copies of the aggregated data to prevent python
    # from incorrectly referencing the dataframe as one
    file_name = 'data/aggregated_2014_to_2019_{}.csv'.format(num_games)
    df_home = pd.read_csv(file_name)
    df_away = pd.read_csv(file_name)  

    merge_game_ids(df_home, df_away, num_games)

if __name__ == '__main__':
    num_games = int(input('Input Number of Games to Aggregate: '))
    merger(num_games)