import pandas as pd 
import numpy as np

def remove_corr_stats(df) -> pd.DataFrame: 
    '''
    Based on EDA, remove highly correlated stats
    inputs
    -------
    df: pd.DataFrame() 

    returns
    -------
    df: pd.DataFrame()
    '''
    columns_to_remove = ['home_passAttempts', 'away_passAttempts', 'home_passYardsPerAtt','away_passYardsPerAtt', \
        'home_passIntPct','away_passIntPct', 'home_pass40Plus', 'away_pass40Plus',\
        'home_sacks_allowed_yards','away_sacks_allowed_yards','home_rush1stDowns', 'away_rush1stDowns',\
        'home_rush40Plus','away_rush40Plus', 'home_recFumbles','away_recFumbles']

    df.drop(columns=columns_to_remove,inplace=True)

    return df