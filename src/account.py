import requests
import json
import api.py

# Player Analyzer isn't endorsed by Riot Games and doesn't reflect the views 
# or opinions of Riot Games or anyone officially involved in producing or 
# managing Riot Games properties. Riot Games, and all associated properties 
# are trademarks or registered trademarks of Riot Games, Inc.

def load_credentials():
    with open('account_info.json', 'r') as file:
        return json.load(file)

def save_credentials(creds):
    with open('account_info.json', 'w') as file:
        json.dump(creds, file, indent=4)

def fetch_puuid(creds):
    url = f'https://{creds["region"]}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{creds["gameName"]}/{creds["tagLine"]}'
    response = requests.get(url, params={'api_key': creds['api_key']})
    return response.json()['puuid']

def main():
    creds = load_credentials()
    
    if 'puuid' not in creds:
        creds['puuid'] = fetch_puuid(creds)
        save_credentials(creds)
        print("puuid saved")

if __name__ == '__main__':
    main()