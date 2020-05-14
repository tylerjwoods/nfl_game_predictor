import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from src.remove_correlated_stats import remove_corr_stats
from sklearn.metrics import recall_score, precision_score, accuracy_score

def calc_poss_winnings(bet, line):
    return bet * line

def gamb_imp(num_games=3, threshold=0.5):
    '''
    Gets the total amount of winnings / losses 
    from the 2019 season based on the model from 2014-2019
    inputs
    -------
    num_games: number of games that is being aggregated across(for example, 3)
    threshold: how certain you want to be of the model.  For example, if you want your model to be 70% sure that either
            the home team will win or 70% sure the away team will win, enter 0.7
    '''
    ### Develop Model ###
    file_name = 'data/merged_games_{}.csv'.format(num_games)

    df_train = pd.read_csv(file_name)
    df_test = pd.read_csv(file_name)
    df_train = df_train[df_train['season']<2019].copy()
    df_test = df_test[df_test['season']>=2019].copy()
    df_train.reset_index(inplace=True, drop=True)
    df_test.reset_index(inplace=True, drop=True)
    df_train = remove_corr_stats(df_train)
    df_test = remove_corr_stats(df_test)

    X_train = np.array(df_train.drop(columns=['game_id', 'season', 'week', 'home_team','away_team','home_win_game']))
    y_train = np.array(df_train.loc[:,'home_win_game'])
    X_test = np.array(df_test.drop(columns=['game_id', 'season', 'week', 'home_team','away_team','home_win_game']))
    y_test = np.array(df_test.loc[:,'home_win_game'])

    model = GradientBoostingClassifier(learning_rate=0.01,
                                   n_estimators=500,
                                   min_samples_leaf=5,
                                   max_depth=2,
                                   subsample=0.5)
    model.fit(X_train, y_train)
    #y_predict = model.predict(X_test)
    #y_true = y_test
    #print("Accuracy:", accuracy_score(y_true, y_predict))
    #print("Precision:", precision_score(y_true, y_predict))
    #print("Recall:", recall_score(y_true, y_predict))

    # Get the probabilities for the different classifications.
    # 0 means that model is predicting away team will win,
    # 1 means that model is predicting home team will win
    proba_away_team_wins = model.predict_proba(X_test)[:,0]
    proba_home_team_wins = model.predict_proba(X_test)[:,1]

    ### Gambling DataFrame ###
    df_gambling = df_test.loc[:,['game_id', 'season', 'week', 'home_team','away_team','home_win_game']]
    df_gambling['proba_away_team_wins'] = proba_away_team_wins
    df_gambling['proba_home_team_wins'] = proba_home_team_wins  

    # This threshold will limit the number of games you gamble on, based on how sure you want 
    # the model to be. For example, if you want your model to be 70% sure that either
    # the home team will win or 70% sure the away team will win, enter 0.7
    #threshold = float(input('Enter how certain you want to be for gambling on your model: '))

    ### Develop DataFrame for Analyzing The Games with only predicted probablities above the requested ###
    df_threshold = df_gambling[(df_gambling['proba_away_team_wins']>threshold) | (df_gambling['proba_home_team_wins']>threshold)].copy()
    df_threshold.reset_index(inplace=True, drop=True)
    # Make a new column prediction that determines which team (home or away) our model predicts based on the 
    # probabilities of the prediction
    df_threshold['prediction'] = (df_threshold['proba_home_team_wins'] > df_threshold['proba_away_team_wins']).astype(int)

    # Calculate accuracy score - Not needed for this purpose but leaving it in just in case
    #accuracy = accuracy_score(np.array(df_threshold['home_win_game']), 
               #np.array(df_threshold['prediction']))

    # Create a result column that determines if our prediction is correct. 1 will be we were correct,
    # 0 is we made incorrect prediction
    df_threshold['result'] = (df_threshold['home_win_game'] == df_threshold['prediction']).astype(int)
    # Replace 0 with -1. Was going to use it for multiplying but I don't think it's necessary.
    df_threshold['result'] = df_threshold['result'].replace(0, -1)

    # Load in the betting lines dataframe that will be used to calculate the amount of money
    # we can win or lose
    betting_lines = pd.read_csv('data/betting_lines.csv')
    betting_lines.drop(columns='Unnamed: 0', inplace=True)


    # Make a new dataframe that is just important info from the betting lines dataframe
    summaried_betting_lines = betting_lines.loc[:,['game_id','season','awayLine','homeLine']].copy()
    summaried_betting_lines['season']= summaried_betting_lines['season'].map(lambda x: x[0:4]).astype(int)
    df_threshold_2019 = df_threshold[df_threshold['season']>2018].copy()

    # merge the threshold dataframe and the summaried betting lines dataframe
    gambling_df = df_threshold_2019.merge(summaried_betting_lines,on='game_id',how='left')

    # Use the american odds to re-calculate the return of the bet.
    # For example, american odds of +200 returns 2-to-1
    # and american odds of -200 returns 0.5 to 1
    gambling_df['awayLine'] = gambling_df['awayLine'].map(lambda x: 100/-x if x < 0 else x)
    gambling_df['homeLine'] = gambling_df['homeLine'].map(lambda x: 100/-x if x < 0 else x)
    gambling_df['awayLine'] = gambling_df['awayLine'].map(lambda x: x/100 if x > 1 else x)
    gambling_df['homeLine'] = gambling_df['homeLine'].map(lambda x: x/100 if x > 1 else x)

    # Calculate the possible winnings. For example, if we place a bet and it is correct, then 
    # the winning bet will be 100 * line that was calculated above
    gambling_df['possible_winnings'] = gambling_df.apply(lambda x: (calc_poss_winnings(100,x['homeLine']) if x['prediction']==1 
                                    else calc_poss_winnings(100,x['awayLine'])),axis=1)

    # Determine if we won or lost. If we won, the column is equal to the possible winnings.
    # If we lost, the column is equal to the bet placed (for example, -100)
    gambling_df['wins_or_loss'] = gambling_df.apply(lambda x: x['possible_winnings'] if x['result']==1 
                                else -100,axis=1)

    #return gambling_df

    # sum the wins_or_loss column to find how much you won over the course of a season
    total = gambling_df['wins_or_loss'].sum()

    return total