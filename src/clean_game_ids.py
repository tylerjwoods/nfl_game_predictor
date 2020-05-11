import pandas as pd 
import numpy as np 

def game_id_cleaner(df_:pd.DataFrame) -> pd.DataFrame:
    '''
    Drops games that do not have a duplicate game_id.
    In 2017, there were 30 games that did not have 
    the complete game for both teams. For example,
    Week 17 of Season 17, NO played TB. The only data
    was for NO and did not have TB, so there is no reason 
    to keep that data.
    '''
    df = df_.copy()

    df.reset_index(drop=True,inplace=True)

    # go through each game_id and store
    # the number of rows that contain that 
    # game_id. Should be 2.
    game_ids = {}
    all_game_ids = df['game_id']
    for each_game_id in all_game_ids:
        if each_game_id not in game_ids:
            game_ids[each_game_id] = 0
        game_ids[each_game_id] += 1

    
    # find the game_ids that only have 1 entry
    single_games = []
    for each_game_id in game_ids:
        if game_ids[each_game_id] < 2:
            single_games.append(each_game_id)

    # drop rows that contain game_ids that only have single entries
    for each_single_game in single_games:
        df.drop(df[df['game_id']==each_single_game].index, inplace=True)

    return df