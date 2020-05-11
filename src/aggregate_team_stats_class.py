import pandas as pd 
import numpy as np

class AggregatedStats():
    '''
    Class that averages stats from previous n_games in a pandas dataframe
    inputs:
    -------
    df: pandas dataframe
    num_games: integer, how many previous games to average across
    
    attributes to use outside of class
    --------
    self.aggregated_stats: pandas dataframe of aggregated stats
    '''

    def __init__(self, df_stats, n_games):
        # df_stats contains similar teams (teams that moved from one location to another),
        # e.g., SD -> LAC, so need to combine those teams first
        self.df_stats = self._combine_sim_teams(df_stats)
        self.n_games = n_games
        
        # call method _team_stats_aggregator and set the aggregated_stats to the return
        # of that method
        self.aggregated_stats = self._team_stats_aggregator()

    def _combine_sim_teams(self, df2):
        '''
        Between the years of 2014 to 2019, some teams changed names / cities. This function
        will rename the teams of previous cities/names to current team name.
        '''
        df = df2.copy()
        # Chargers moved from SD to LAC
        df.loc[(df['team'] =='SD'),'team'] = 'LAC'
        df.loc[(df['opponent'] =='SD'),'opponent'] = 'LAC'
        
        # Rams moved from STL to LA
        df.loc[(df['team'] =='STL'),'team'] = 'LA'
        df.loc[(df['opponent'] =='STL'),'opponent'] = 'LA'

        # Call _game_id_cleaner method due to some games not being complete.
        df = _game_id_cleaner(df)

        return df

    def _game_id_cleaner(df_:pd.DataFrame) -> pd.DataFrame:
        '''
        Drops games that do not have a duplicate game_id.
        In 2017, there were 30 games that did not have 
        the complete game for both teams. For example,
        Week 17 of Season 17, NO played TB. The only data
        was for NO and did not have TB, so there is no reason 
        to keep that data.
        '''
        df = df_.copy()

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

    def _team_stats_aggregator(self):
        '''
        inputs:
        -------
        none
        
        returns
        ------
        df: pandas dataframe with aggregated stats for all teams
        '''

        # make new dataframe to store aggregated stats, will be concated for each team
        agg_games = pd.DataFrame()
        df = self.df_stats.copy()

        # grab each team from dataframe and pass to agg_game_stats function
        # concat agg_games with each teams' aggregated stats
        for each_team in df['team'].unique():
            print(each_team)
            team_df = df.loc[(df['team'] ==each_team), :].reset_index()
            agg_games_stats_each_team = self._agg_game_stats(team_df)
            agg_games = pd.concat([agg_games,agg_games_stats_each_team])
        agg_games.reset_index(inplace=True)

        # return agg_games with all of the teams and their aggregated stats
        return agg_games

    
    
    def _agg_game_stats(self, df_each_team):
        '''
        inputs:
        -------
        None
        
        returns:
        --------
        df: pandas dataframe with aggregated stats for all teams
        '''
        # The playing at home column is the last column that will not be 
        # used for analysis. Need to find that column in the dataframe.
        playing_at_home_column = np.where(df_each_team.columns.values == 'playing_at_home')
        playing_at_home_column = int(playing_at_home_column[0])

        # get the total number of rows from the dataframe
        all_rows = len(df_each_team)

        # make a copy of the df_stats
        df = df_each_team.copy()

        # loop through each stat(column), for each stat, take the mean of the 
        # previous n_games and store it in df.
        for each_column in df.columns.values[playing_at_home_column+1:-1]:
            for each_row in range(self.n_games, all_rows):
                df.loc[each_row, each_column] = df_each_team.loc[each_row-self.n_games:each_row-1,each_column].mean()

        # same thing for wins, except sum the previous n_games rather than take the mean
        df['wins_past_games'] = 0
        for each_row in range(self.n_games, all_rows):
            df.loc[each_row, 'wins_past_games'] = df_each_team.loc[each_row-self.n_games:each_row-1,'win_game'].sum()

        # Drop the first n_games since not able to take average of previous n_games
        # e.g., the first game of ARI from 2014 - don't have data fromn 2013 season 
        # so can't take the previous games averages
        df.drop(index=range(0,self.n_games), inplace=True)

        return df

        