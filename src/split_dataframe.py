import pandas as pd 
import numpy as np

def split_df(df_:pd.DataFrame(), test_percentage:float=0.3) -> pd.DataFrame():
    '''
    splits a pandas dataframe but keeps games together. i.e., a game
    played between ARI and SEA will either be grouped into the
    test or the train

    inputs
    -------
    df_: pandas dataframe
    test_percentage: the percentage of the dataframe that will be assigned to test

    returns
    -------
    df_train, df_test: pandas dataframes
    '''
    df = df_.copy()

    # initialize two dataframes to store the train and the test
    df_train = pd.DataFrame()
    df_test = pd.DataFrame()

    # sort the dataframe by the game_id
    df = df.sort_values(by='game_id').reset_index(drop=True)

    # loop through each game_id, check to see if a random number
    # is greater than the test_percentage
    # if is, assign it to train, otherwise assign it to test

    for i in range(0, len(df), 2):
        if np.random.rand() > test_percentage:
            df_train = pd.concat([df_train, df.loc[i:i+1,:]])
        else:
            df_test = pd.concat([df_test, df.loc[i:i+1,:]])

    return df_train, df_test

