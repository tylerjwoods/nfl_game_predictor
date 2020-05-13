import numpy as np
import requests
import pandas as pd
import json
from requests.auth import HTTPBasicAuth
import copy

def get_bet_lines() -> None:
    '''
    Uses mysportsfeeds API to get each game's betting lines and stores
    it in a CSV for later use.
    '''
    # Get User API key and Password
    user = input('Enter API Key: ') #API Key from mysportsfeeds
    password = input('Enter Password: ') #Password from mysportsfeeds 

    # Create dictionary that will be template for storing response
    new_record = {
        'game_id': None,
        'season': None,
        'week': None,
        'awayTeam': None,
        'homeTeam': None,
        'awayLine': None,
        'homeLine': None
        }
    # Create list to store all of the records in
    all_records = []

    weeks = list(range(1,18))

    seasons = [2019]

    # Loop thru each season and week. Obtain opening game lines
    for each_season in seasons:
        season = '{}-{}-regular'.format(each_season,each_season+1)
        for each_week in weeks:
            url = f"https://api.mysportsfeeds.com/v2.1/pull/nfl/{season}/week/{each_week}/odds_gamelines.json"
            res = requests.get(url, auth=HTTPBasicAuth(user, password))
            text_ = json.loads(res.text)

            for i, each_game in enumerate(text_['gameLines']):
                game_record = new_record.copy()
                game_record['game_id'] = text_['gameLines'][i]['game']['id']
                game_record['season'] = season
                game_record['week'] = text_['gameLines'][i]['game']['week']
                game_record['awayTeam'] = text_['gameLines'][i]['game']['awayTeamAbbreviation']
                game_record['homeTeam'] = text_['gameLines'][i]['game']['homeTeamAbbreviation']
                game_record['awayLine'] = text_['gameLines'][i]['lines'][0]['moneyLines'][0]['moneyLine']['awayLine']['american']
                game_record['homeLine'] = text_['gameLines'][i]['lines'][0]['moneyLines'][0]['moneyLine']['homeLine']['american']
                all_records.append(game_record)

    df = pd.DataFrame(all_records)

    df.to_csv('../data/betting_lines.csv')

