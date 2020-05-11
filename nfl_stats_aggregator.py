import numpy as np
import pandas as pd

from src.aggregate_team_stats_class import AggregatedStats
from src.get_team_stats import YearlyTeamStats
from src.clean_game_ids import game_id_cleaner

def get_stats():
    '''
    Using YearlyTeamStats class, get team stats for each
    year and store into a dataframe.
    Then store all of the seasons into one dataframe.
    '''
    user = input('Enter API Key: ') #API Key from mysportsfeeds
    password = input('Enter Password: ') #Password from mysportsfeeds 

    year = 2019
    stats_2019 = YearlyTeamStats(year, user, password)
    stats_2019.team_stats.to_csv('data/stats_2019.csv')

    year = 2018
    stats_2018 = YearlyTeamStats(year, user, password)
    stats_2018.team_stats.to_csv('data/stats_2018.csv')

    year = 2017
    stats_2017 = YearlyTeamStats(year, user, password)
    stats_2017.team_stats.to_csv('data/stats_2017.csv')

    year = 2016
    stats_2016 = YearlyTeamStats(year, user, password)
    stats_2016.team_stats.to_csv('data/stats_2016.csv')

    year = 2015
    stats_2015 = YearlyTeamStats(year, user, password)
    stats_2015.team_stats.to_csv('data/stats_2015.csv')

    year = 2014
    stats_2014 = YearlyTeamStats(year, user, password)
    stats_2014.team_stats.to_csv('data/stats_2014.csv')

    all_seasons = pd.concat([stats_2014.team_stats, stats_2015.team_stats, stats_2016.team_stats, stats_2017.team_stats, stats_2018.team_stats, stats_2019.team_stats])
    all_seasons.drop(columns='Unnamed: 0', inplace=True)

    # Store all_seasons into a csv file for use later
    all_seasons.to_csv('data/stats_2014_to_2019.csv', index=False)

def main():
    # Make call to function get_stats
    get_stats()

    # Get the dataframe that was created by get_stats function
    df = pd.read_csv('data/stats_2014_to_2019.csv')

    # Clean out the rows that do not have duplicate game_ids
    df = game_id_cleaner(df)

    # Aggregate team stats using AggregatedStats class
    team_stats_aggregated = AggregatedStats(df, 6)

    # Drop columns that are not needed
    columns_to_drop = ['level_0','index']
    for column_to_drop in columns_to_drop:
        try:
            team_stats_aggregated.aggregated_stats.drop(columns=column_to_drop, inplace=True)
        except:
            pass
    
    # Store the aggregated stats into a csv file for later use
    team_stats_aggregated.aggregated_stats.to_csv('data/aggregated_2014_to_2019.csv', index=False)

if __name__ == '__main__':
    main()