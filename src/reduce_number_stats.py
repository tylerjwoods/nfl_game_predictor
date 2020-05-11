import pandas as pd 

def clean_team_stats(df):
    '''
    inputs
    ------
    df: pandas dataframe

    returns
    ------
    df: pandas dataframe with cleaned dataset. drops multiple columns from original df
    '''
    # For first analysis, let's drop most of the columns to make our program run faster
    columns_to_drop = ['passCompletions', 'passAvg', 'passYardsPerAtt', 'rushYards', 'passIntPct', 'passLng', \
        'pass20Plus', 'pass40Plus', 'sacks_allowed_yards', 'rushAverage', 'rushLng', 'rush1stDowns', 'rush1stDownsPct',\
        'rush20Plus','rush40Plus', 'rushFumbles','rec1stDowns','recFumbles','tackleSolo','tackleTotal','tackleAst',\
        'sackYds','tacklesForLoss', 'krTD', 'kr20Plus', 'fgMade','field_goal_pct','punt_inside_20_pct','third_down_pct',
        'fourth_down_pct','penalties']

    df.drop(columns=columns_to_drop,inplace=True)

    return df