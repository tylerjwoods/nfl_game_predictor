import numpy as np
import pandas as pd
import copy

def merge_game_ids(df_1, df_2):
    '''
    Merges df_home and df_away into one 
    dataframe for analysis
    df_1 & df_2: pandas dataframe with all of the rows. Need two copies of the dataframe
    due to odd things going on with pandas and copies of dataframes
    '''
    # Create copies of dataframes
    home_df = df_1.copy()
    away_df = df_2.copy()

    mask = home_df['playing_at_home'] == 1
    home_df = home_df.loc[mask, :].copy()
    away_df = away_df.loc[~mask, :].copy()

    # Drop columns that are not needed
    away_df.drop(columns=['season','week','opponent','playing_at_home','win_game'],inplace=True)
    home_df.drop(columns=['opponent','playing_at_home'],inplace=True)

    # Set Column names to home_team / away_team
    home_df.columns.values[3] = 'home_team'
    away_df.columns.values[1] = 'away_team'

    ### AWAY TEAM ###
    # Create a new dataframe to store the away_team stats
    away=pd.DataFrame()
    # Create a dictionary to rename the column names
    away_dict = {}
    for each_column in away_df.columns.values[2:]:
        away_dict[each_column] = f'away_{each_column}'

    # Fill in away dataframe with stats
    away['game_id'] = away_df.loc[:,'game_id']
    away['away_team'] = away_df.iloc[:,1]
    for each_stat in away_dict:
        away[away_dict[each_stat]] = away_df[each_stat]

    ### HOME TEAM ###
    # Do same thing for home team
    home=pd.DataFrame()
    home_dict = {}
    for each_column in home_df.columns.values[4:]:
        home_dict[each_column] = f'home_{each_column}'
    home['game_id'] = home_df.loc[:,'game_id']
    home['season'] = home_df.loc[:,'season']
    home['week'] = home_df.loc[:,'week']
    home['home_team'] = home_df.iloc[:,3]
    for each_stat in home_dict:
        home[home_dict[each_stat]] = home_df[each_stat]

    ### COMBINE ###
    full_df = home.merge(away,how='left',on='game_id')
    # Organize the dataframe columns
    full_organized = pd.DataFrame()
    full_organized['game_id'] = full_df.pop('game_id')
    full_organized['season'] = full_df.pop('season')
    full_organized['week'] = full_df.pop('week')
    full_organized['home_team'] = full_df.pop('home_team')
    full_organized['away_team'] = full_df.pop('away_team')
    full_organized['home_win_game'] = full_df.pop('home_win_game')

    for each_column in full_df.columns.values:
        full_organized[each_column] = full_df.loc[:,each_column]

    # Store dataframe in a CSV for later use
    full_organized.to_csv('data/merged_games.csv',index=False)