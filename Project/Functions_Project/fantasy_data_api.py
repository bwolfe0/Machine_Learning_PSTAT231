import json
import requests

from dotenv import load_dotenv
import os

import pandas as pd

def get_data(
    season_year,
    week,api_key,
    endpoint_prefix='TeamGameStats'):
    '''
    Parameters
    ----------

    Returns
    -------
    '''
    base_url = 'https://api.sportsdata.io/api/nfl/odds/json'
    endpoint = f'/{endpoint_prefix}/{season_year}/{week}'
    header = {'Ocp-Apim-Subscription-Key': api_key}

    response = requests.get(base_url + endpoint, headers=header)

    if response.status_code != 200:
        return f"Error: {response.status_code}"
    
    if endpoint_prefix == 'GameOddsByWeek':
        betting_data = pd.DataFrame(json.loads(response.text))
        for idx in range(len(betting_data.index)):
            #Create columns for the spreads and payouts from the 'PregameOdds' column's dictionary
            betting_data.at[idx, 'HomePointSpread'] = betting_data.at[idx,'PregameOdds'][0]['HomePointSpread']
            betting_data.at[idx,'AwayPointSpread'] = betting_data.at[idx,'PregameOdds'][0]['AwayPointSpread']
            betting_data.at[idx,'HomePointSpreadPayout'] = betting_data.at[idx,'PregameOdds'][0]['HomePointSpreadPayout']
            betting_data.at[idx,'AwayPointSpreadPayout'] = betting_data.at[idx,'PregameOdds'][0]['AwayPointSpreadPayout']

            #Extract result of spread
            if (betting_data.at[idx,'HomeTeamScore'] - betting_data.at[idx,'HomePointSpread']) > betting_data.at[idx,'AwayTeamScore']:
                betting_data.at[idx, 'SpreadResult'] = 'Home'
            elif (betting_data.at[idx,'HomeTeamScore'] - betting_data.at[idx,'HomePointSpread']) == betting_data.at[idx,'AwayTeamScore']:
                betting_data.at[idx, 'SpreadResult'] = 'Push'
            else:
                betting_data.at[idx, 'SpreadResult'] = 'Away'

        betting_data.drop('PregameOdds', axis=1, inplace=True)
        return betting_data

    return pd.DataFrame(json.loads(response.text))