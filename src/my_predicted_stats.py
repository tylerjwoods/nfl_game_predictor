import pandas as pd 

def my_pred_stats(df):
    '''
    returns only the stats that, using my domain knowledge,
    would be important to winning the game
    inputs
    ------
    df: pandas dataframe

    returns
    ------
    df: pandas dataframe with cleaned dataset. drops multiple columns from original df
    '''
    df_ = df[['game_id','season','week','team','opponent','team_score','qb_rating','sacks','playing_at_home', 'interceptions',\
        'opponent_score','fumbles','wins_past_games','passTD','passInt','win_game']]


    return df_