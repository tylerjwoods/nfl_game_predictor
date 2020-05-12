import numpy as np
import pandas as pd

from src.get_team_game_stats import YearlyTeamStats

def get_stats() -> None:
    '''
    Using YearlyTeamStats class, get team stats for each
    year and store into a dataframe.
    Then store all of the seasons into one dataframe and save to CSV file.
    '''
    user = input('Enter API Key: ') #API Key from mysportsfeeds
    password = input('Enter Password: ') #Password from mysportsfeeds 

    year = 2019
    stats_2019 = YearlyTeamStats(year, user, password)
    stats_2019.team_stats.to_csv('../data/stats_2019.csv')

    year = 2018
    stats_2018 = YearlyTeamStats(year, user, password)
    stats_2018.team_stats.to_csv('../data/stats_2018.csv')

    year = 2017
    stats_2017 = YearlyTeamStats(year, user, password)
    stats_2017.team_stats.to_csv('../data/stats_2017.csv')

    year = 2016
    stats_2016 = YearlyTeamStats(year, user, password)
    stats_2016.team_stats.to_csv('../data/stats_2016.csv')

    year = 2015
    stats_2015 = YearlyTeamStats(year, user, password)
    stats_2015.team_stats.to_csv('../data/stats_2015.csv')

    year = 2014
    stats_2014 = YearlyTeamStats(year, user, password)
    stats_2014.team_stats.to_csv('../data/stats_2014.csv')

    all_seasons = pd.concat([stats_2014.team_stats, stats_2015.team_stats, stats_2016.team_stats, stats_2017.team_stats, stats_2018.team_stats, stats_2019.team_stats])
    all_seasons.drop(columns='Unnamed: 0', inplace=True)

    # Store all_seasons into a csv file for use later
    all_seasons.to_csv('../data/stats_2014_to_2019.csv', index=False)
