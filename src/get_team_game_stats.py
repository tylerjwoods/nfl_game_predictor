import requests
import pandas as pd
import json
from requests.auth import HTTPBasicAuth

class YearlyTeamStats():
    '''
    Class that gets the yearly stats for all teams for each game played.
    Inputs
    -------
    year: # String or Int Year to get the stats for (2014 - 2019)
    user: api_key # String, API Key from mysportsfeeds.com
    password: String, Password from mysportsfeeds.com

    Attributes to use outside of class
    --------------------------
    team_stats: Pandas Dataframe that holds teams' stats for given year
    '''
    def __init__(self, year, api_key, password):
        self.year = int(year) # Int, Year to get the stats for (2014 - 2019)
        self.user = api_key # String, API Key from mysportsfeeds.com
        self.password = password # String, Password from mysportsfeeds.com
        self.team_stats = self._get_stats() # Dataframe that holds teams' stats for given year

    def _get_stats(self):
        '''
        Method to call mysportsfeeds API then passes the json object to _parse data. Returns the dataframe from
        _parse_data back to self.team_stats.
        '''

        team_names = self._get_team_names()
        url = 'https://api.mysportsfeeds.com/v2.1/pull/nfl/{}-regular/team_gamelogs.json'.format(self.year)
        params = {'team':team_names}
        res = requests.get(url, params=params,auth=HTTPBasicAuth(self.user, self.password)) # JSON object with the data
        
        # dump the json into a file
        season_json = json.loads(res.text)
        json_obj = json.dumps(season_json)
        with open('nfl_json_files/team_game_logs_{}.json'.format(self.year),'w') as json_file:
            json_file.write(json_obj)

        # Call _parse_data to filter JSON object data
        year_team_stats = self._parse_data(res)

        return year_team_stats

    def _get_team_names(self):
        '''
        Since team names/locations and abbrevations can change from year-to-year (e.g., SD -> LAC), 
        need to get the list of team names for that year
        '''
        url = 'https://api.mysportsfeeds.com/v2.1/pull/nfl/{}-{}-regular/games.json'.format(self.year, self.year+1)
        res = requests.get(url, auth=HTTPBasicAuth(self.user, self.password))
        json_team_names = json.loads(res.text)

        team_names = []
        for i in range(0,16):
            team_names.append(json_team_names['games'][i]['schedule']['homeTeam']['abbreviation'])
            team_names.append(json_team_names['games'][i]['schedule']['awayTeam']['abbreviation'])
        team_names.sort()
        team_names = ','.join(team_names)
        return team_names
        
    def _parse_data(self, res):
        '''
        Takes res which is a JSON object and parses the data into stats that will be used for modeling.
        '''
        season_json = json.loads(res.text)

        team_gamelogs = pd.DataFrame()
        for i in range(0,len(season_json['gamelogs'])):
            df = pd.DataFrame()
            # Get the Game ID, Week, Team, Opponent
            df['game_id'] = [season_json['gamelogs'][i]['game']['id']]
            df['season'] = self.year
            df['week'] = season_json['gamelogs'][i]['game']['week']
            df['team'] = season_json['gamelogs'][i]['team']['abbreviation']
            if season_json['gamelogs'][i]['game']['awayTeamAbbreviation'] == season_json['gamelogs'][i]['team']['abbreviation']:
                df['opponent'] = season_json['gamelogs'][i]['game']['homeTeamAbbreviation']
            else:
                df['opponent'] = season_json['gamelogs'][i]['game']['awayTeamAbbreviation']
            
            # Get if team is home, 1 if home, 0 if away
            if season_json['gamelogs'][i]['team']['abbreviation'] == season_json['gamelogs'][i]['game']['homeTeamAbbreviation']:
                df['playing_at_home'] = 1
            else:
                df['playing_at_home'] = 0
                
            # Get Stats that will be used for analysis
            ## Passing stats
            df['passAttempts'] = season_json['gamelogs'][i]['stats']['passing']['passAttempts']
            df['passCompletions'] = season_json['gamelogs'][i]['stats']['passing']['passCompletions']
            df['passPct'] = season_json['gamelogs'][i]['stats']['passing']['passPct']
            df['passGrossYards'] = season_json['gamelogs'][i]['stats']['passing']['passGrossYards']
            df['passAvg'] = season_json['gamelogs'][i]['stats']['passing']['passAvg']
            df['passYardsPerAtt'] = season_json['gamelogs'][i]['stats']['passing']['passYardsPerAtt']
            df['passTD'] = season_json['gamelogs'][i]['stats']['passing']['passTD']
            df['passInt'] = season_json['gamelogs'][i]['stats']['passing']['passInt']
            df['passIntPct'] = season_json['gamelogs'][i]['stats']['passing']['passIntPct']
            df['passLng'] = season_json['gamelogs'][i]['stats']['passing']['passLng']
            df['pass20Plus'] = season_json['gamelogs'][i]['stats']['passing']['pass20Plus']
            df['pass40Plus'] = season_json['gamelogs'][i]['stats']['passing']['pass40Plus']
            df['sacks_allowed'] = season_json['gamelogs'][i]['stats']['passing']['passSacks']
            df['sacks_allowed_yards'] = season_json['gamelogs'][i]['stats']['passing']['passSackY']
            df['qb_rating'] = season_json['gamelogs'][i]['stats']['passing']['qbRating']

            ## Rushing stats
            df['rushAttempts'] = season_json['gamelogs'][i]['stats']['rushing']['rushAttempts']
            df['rushYards'] = season_json['gamelogs'][i]['stats']['rushing']['rushYards']
            df['rushAverage'] = season_json['gamelogs'][i]['stats']['rushing']['rushAverage']
            df['rushLng'] = season_json['gamelogs'][i]['stats']['rushing']['rushLng']
            df['rush1stDowns'] = season_json['gamelogs'][i]['stats']['rushing']['rush1stDowns']
            df['rush1stDownsPct'] = season_json['gamelogs'][i]['stats']['rushing']['rush1stDownsPct']
            df['rush20Plus'] = season_json['gamelogs'][i]['stats']['rushing']['rush20Plus']
            df['rush40Plus'] = season_json['gamelogs'][i]['stats']['rushing']['rush40Plus']
            df['rushFumbles'] = season_json['gamelogs'][i]['stats']['rushing']['rushFumbles']

            ## Receiving Stats
            df['rec1stDowns'] = season_json['gamelogs'][i]['stats']['receiving']['rec1stDowns']
            df['recFumbles'] = season_json['gamelogs'][i]['stats']['receiving']['recFumbles']

            ## Tackles Stats
            df['tackleSolo'] = season_json['gamelogs'][i]['stats']['tackles']['tackleSolo']
            df['tackleTotal'] = season_json['gamelogs'][i]['stats']['tackles']['tackleTotal']
            df['tackleAst'] = season_json['gamelogs'][i]['stats']['tackles']['tackleAst']
            df['sacks'] = season_json['gamelogs'][i]['stats']['tackles']['sacks']
            df['sackYds'] = season_json['gamelogs'][i]['stats']['tackles']['sackYds']
            df['tacklesForLoss'] = season_json['gamelogs'][i]['stats']['tackles']['tacklesForLoss']

            # Interceptions Stats
            df['interceptions'] = season_json['gamelogs'][i]['stats']['interceptions']['interceptions']

            # Fumbles
            df['fumbles'] = season_json['gamelogs'][i]['stats']['fumbles']['fumbles']

            # Kickoff Returns
            df['krTD'] = season_json['gamelogs'][i]['stats']['kickoffReturns']['krTD']
            df['kr20Plus'] = season_json['gamelogs'][i]['stats']['kickoffReturns']['kr20Plus']

            # Field Goals
            df['fgMade'] = season_json['gamelogs'][i]['stats']['fieldGoals']['fgMade']
            df['field_goal_pct'] = season_json['gamelogs'][i]['stats']['fieldGoals']['fgPct']

            # Punting
            df['punt_inside_20_pct'] = season_json['gamelogs'][i]['stats']['punting']['puntIn20Pct']

            ## Miscellaneous stats
            df['third_down_pct'] = season_json['gamelogs'][i]['stats']['miscellaneous']['thirdDownsPct']
            df['fourth_down_pct'] = season_json['gamelogs'][i]['stats']['miscellaneous']['fourthDownsPct']
            df['penalties'] =  season_json['gamelogs'][i]['stats']['miscellaneous']['penalties']

            # Final Scores
            df['team_score'] = season_json['gamelogs'][i]['stats']['standings']['pointsFor']
            df['opponent_score'] = season_json['gamelogs'][i]['stats']['standings']['pointsAgainst']
        
            # Result - Target, Whether or not the team won
            df['win_game'] = season_json['gamelogs'][i]['stats']['standings']['wins']
            
            # Append / Concat the next line of the dataframe
            team_gamelogs = pd.concat([team_gamelogs, df])
            
        team_gamelogs.reset_index(drop=True, inplace=True)

        return team_gamelogs