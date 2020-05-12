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
    df_ = df[['game_id','season','week','home_team','away_team','home_win_game','home_team_score','away_team_score',\
        'home_qb_rating','away_qb_rating','home_sacks','away_sacks', 'home_interceptions','away_interceptions',\
        'home_opponent_score','away_opponent_score','home_fumbles','away_fumbles',\
        'home_wins_past_games','away_wins_past_games','home_passTD','away_passTD','home_passInt', 'away_passInt']]


    return df_