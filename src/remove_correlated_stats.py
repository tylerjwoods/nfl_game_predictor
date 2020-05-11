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
    columns_to_remove = ['passAttempts', 'passYardsPerAtt', 'passIntPct', 'pass40Plus', 'sacks_allowed_yards',\
        'rush1stDowns', 'rush40Plus', 'recFumbles']

    df.drop(columns=columns_to_remove,inplace=True)

    return df