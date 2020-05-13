import numpy as np
import pandas as pd

from src.aggregate_team_stats_class import AggregatedStats
from src.clean_game_ids import game_id_cleaner

def aggregator():
    '''
    From the function 'obtain_stats.py', the stats_2014_to_2019.csv file was created
    and stored in the data/ folder.

    The function game_id_cleaner gets rid of incomplete data (missing either the home team and away team)

    The class AggregatedStats takes the average of stats from n_games. 

    This function then ensures that each game has a complete set then stores the dataframe into
    a CSV 'data/aggregated_2014_to_2019.csv'
    '''
    # Get the dataframe that was created by get_stats function
    df = pd.read_csv('data/stats_2014_to_2019.csv')

    # Clean out the rows that do not have duplicate game_ids
    df = game_id_cleaner(df)
    
    num_games = int(input('Input Number of Games to Aggregate: '))

    # Aggregate team stats using AggregatedStats class
    team_stats_aggregated = AggregatedStats(df, num_games)

    # Drop columns that are not needed
    columns_to_drop = ['level_0','index']
    for column_to_drop in columns_to_drop:
        try:
            team_stats_aggregated.aggregated_stats.drop(columns=column_to_drop, inplace=True)
        except:
            pass
        
    # Clean out rows again, just to ensure we have correct games
    df = team_stats_aggregated.aggregated_stats
    df = game_id_cleaner(df)
    
    # Store the aggregated stats into a csv file for later use
    file_name = 'data/aggregated_2014_to_2019_{}.csv'.format(num_games)
    df.to_csv(file_name, index=False)

if __name__ == '__main__':
    aggregator()