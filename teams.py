import pandas as pd
import numpy as np
import pandasql as ps
import json
import csv
import os
from functools import reduce
import inspect, re

#Takes a master list of all matches for all users
#Creates separate DF for each user
#Creates a user specific list of games with teammates columns

def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)

def create_full_agg(pewpers):

    field_names = ["matchID", "user", "mode", "team_rank", "start", "end","kills",
        "medalXp",
        "objectiveTeamWiped",
        "matchXp",
        "scoreXp",
        "wallBangs",
        "score",
        "totalXp",
        "headshots",
        "assists",
        "challengeXp",
        "rank",
        "scorePerMinute",
        "distanceTraveled",
        "teamSurvivalTime",
        "deaths",
        "objectiveMunitionsBoxTeammateUsed",
        "objectiveBrDownEnemyCircle1","objectiveBrDownEnemyCircle2","objectiveBrDownEnemyCircle3","objectiveBrDownEnemyCircle4", "objectiveBrDownEnemyCircle5","objectiveBrDownEnemyCircle6",
        "kdRatio",
        "objectiveBrMissionPickupTablet",
        "bonusXp",
        "objectiveBrKioskBuy",
        "gulagDeaths",
        "timePlayed",
        "executions",
        "gulagKills",
        "nearmisses",
        "objectiveBrCacheOpen",
        "percentTimeMoving",
        "miscXp",
        "longestStreak",
        "teamPlacement",
        "damageDone",
        "damageTaken",
        "objectiveLastStandKill",
        "objectivePerkMarkedTarget",
        "objectiveDestroyedEquipment",
        "objectiveReviver",
        "objectiveTrophyDefense",
        "objectiveAssistDecoy",
        "objectiveEmpedPlayer",
        "objectiveBinocularsMarked", "objectiveShieldDamage", "objectiveBrC130BoxOpen",
        "objectiveDestroyedVehicleHeavy", "objectiveMedalScoreKillSsManualTurret", "objectiveMedalScoreKillSsRadarDrone",
        "objectiveDestroyedVehicleLight","objectiveMedalScoreSsKillTomaStrike", "objectiveDestroyedVehicleMedium", 
        "objectivePlunderCashBloodMoney", "objectiveMedalScoreSsKillPrecisionAirstrike", "objectiveManualFlareMissileRedirect",
        "objectiveMedalScoreSsKillJuggernaut", "objectiveMedalScoreSsKillManualTurret", 'objectiveBrLootChopperBoxOpen', "objectiveWeaponDropTeammateUsed"]

    # Match Types not to add to stats
    filter_matches = ['br_dmz_plnbld',
                'br_dmz_plndcndy',
                'br_dmz_plndtrios',
                'br_dmz_plndval1',
                'br_dmz_plunquad',
                'brtdm_rmbl',
                'br_kingslayer_kingsltrios'
    ]

    # create list (not used currently)
    # other_modes = [ 'br_mini_miniroyale',
    #     'br_mini_rebirth_mini_royale_duos',
    #     'br_mini_rebirth_mini_royale_solo',
    #     'br_rebirth_rbrthtrios',
    #     'br_truckwar_trwarsquads',
    # ]
    # pewpers = ['DirtyUndies', 'cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator']

    directory = r'./all_matches'
    bad_files = []

    #CSV to create
    print('Creating all_match_data.csv ....')
    with open('all_match_data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        # List of Full Match Files
        print('Searching for pewpers in all collected matches...')
        for filename in os.listdir(directory):
            fullPath = os.path.join(directory, filename)
            
            if filename.endswith(".json") :
                with open(fullPath) as f:
                    match = json.load(f)

            players = match['allPlayers']

            for p in players:
                try:
                    mode = str(p['mode'])
                    # REMOVE PLUNDER AND RUMBLE MATCHES
                    if mode not in filter_matches:
                        if p['player']['username'] in pewpers:
                            entry = {}
                            entry['user']= p['player']['username']
                            entry['matchID'] = p['matchID']
                            entry['mode'] = p['mode']
                            try:
                                entry['team_rank'] = p['player']['rank']
                            except:
                                entry['team_rank'] = 0
                            entry['start'] = p['utcStartSeconds']
                            entry['end'] = p['utcEndSeconds']
                            
                            #print(entry)
                            # print(matchID, mode, user, team_rank, start, end )
                            # writer.writerow([matchID, mode, user, team_rank, start, end ])

                            for key in p['playerStats']:
                                entry[key] = p['playerStats'][key]
                                # print(key, '->', p['playerStats'][key])
                                # stats.append(p['playerStats'][key])
                            writer.writerow(entry)

                except Exception as e:
                    print(fullPath)
                    print(e)
                    if filename not in bad_files:
                        bad_files.append(filename)
    print(bad_files)



def create_user_files(pewpers):

    #Import CSV into Pandas DF
    df = pd.read_csv (r'all_match_data.csv')

    #Season Conditions
    conditions = [
        (df['start'] <= 1581400800), #mw_1
        (df['start'] > 1581400800) & (df['start'] <= 1586235600), #mw_2
        (df['start'] > 1586235600) & (df['start'] <= 1591765200), #mw_3
        (df['start'] > 1591765200) & (df['start'] <= 1596603600), #mw_4
        (df['start'] > 1596603600) & (df['start'] <= 1601355600), #mw_5
        (df['start'] > 1601355600) & (df['start'] <= 1608098400), #mw_6
        (df['start'] > 1608098400) & (df['start'] <= 1614232800), #cw_1
        (df['start'] > 1614232800) #cw_2
        ]

    seasons = ['mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']

    # create a new column and use np.select to assign values to it using our lists as arguments
    df['season'] = np.select(conditions, seasons)

    #Summarize downs
    df['objectiveBrDownEnemyCircle1']= df['objectiveBrDownEnemyCircle1'].fillna(0)
    df['objectiveBrDownEnemyCircle2']= df['objectiveBrDownEnemyCircle2'].fillna(0)
    df['objectiveBrDownEnemyCircle3']= df['objectiveBrDownEnemyCircle3'].fillna(0)
    df['objectiveBrDownEnemyCircle4']= df['objectiveBrDownEnemyCircle4'].fillna(0)
    df['objectiveBrDownEnemyCircle5']= df['objectiveBrDownEnemyCircle5'].fillna(0)
    df['objectiveBrDownEnemyCircle6']= df['objectiveBrDownEnemyCircle6'].fillna(0)
    
    df['downs'] = df.apply(lambda df: df.objectiveBrDownEnemyCircle1 + df.objectiveBrDownEnemyCircle2 + df.objectiveBrDownEnemyCircle3 + df.objectiveBrDownEnemyCircle4 + df.objectiveBrDownEnemyCircle5 + df.objectiveBrDownEnemyCircle6,  axis=1)

    #Rename old modes
    df['mode'].mask(df['mode'] == 'br_25', 'br_brtrios', inplace=True)
    df['mode'].mask(df['mode'] == 'br_87', 'br_brsolo', inplace=True)
    df['mode'].mask(df['mode'] == 'br_88', 'br_brduos', inplace=True)
    df['mode'].mask(df['mode'] == 'br_89', 'br_brquads', inplace=True)

    #Create data_frames list
    dfs = []
    
    #Create User_DF
    for p in pewpers:
        # print(p)
        user_df = df[df['user'].str.match(p)]
        user_df = user_df.sort_values(by=['matchID'])
        user_df = user_df.set_index('matchID',drop=False)
        #print(user_df.index)
        #print(user_df)
        # compile the list of dataframes you want to merge
        dfs.append(user_df)

    g2 = df.groupby(['matchID']).agg(lambda col: ','.join(col))
    g2 = g2.sort_values(by=['matchID'])

    for d in dfs:
        d['teammate1'] = g2['user']
        d[['teammate1','teammate2','teammate3', 'teammate4']] = d.teammate1.str.split(',',expand=True) 
    
        #create cumulative totals

        d = cumtotals(d, seasons)

        # print(d)
        #print(d.iloc[0]['user'])
        file_name = str('user_files/'+d.iloc[0]['user']+ '.csv')
        print('Create file: ' + file_name)
        d.to_csv(file_name, index=False)



def cumtotals(df, seasons):

    df = df.sort_values(by=['start'])
    df = df.set_index('matchID',drop=False)
    df.reset_index(inplace=True, drop=True)

    #create cumulative totals
    
    df['total_kills'] = df.kills.cumsum()
    df['total_deaths'] = df.deaths.cumsum()
    df['total_headshots'] = df.headshots.cumsum()
    df['total_headshotPct'] = df.total_headshots / df.total_kills
    df['total_kd'] = df.total_kills / df.total_deaths
    df['kd_last50'] = df['total_kd'].rolling(50).mean()

    df['total_gulagKills'] = df.gulagKills.cumsum()
    df['total_gulagDeaths'] = df.gulagDeaths.cumsum()
    df['total_gulag_winPct'] = df.total_gulagKills / (df.total_gulagKills + df.total_gulagDeaths)
    df['gulag_last50'] = df['total_gulag_winPct'].rolling(50).mean()

    dfs =[]
    for s in seasons:
        col_name = str(s) + '_kd_last50'
        #print(col_name)
        df1 = df[df['season'] == s]
        #print(len(df1))
        if (len(df1) == 0):
            
            df1['season_kills'] = 0
            df1['season_deaths'] = 0
            df['season_headshots'] = 0
            df['season_headshotPct'] = 0
            df1['season_kd'] = 0
            df1['season_gulagKills'] = 0
            df1['season_gulagDeaths'] = 0
            df1['season_gulag_winPct'] = 0

        else:
            df1['season_kills'] = df.groupby('season')['kills'].cumsum()
            df1['season_deaths'] = df.groupby('season')['deaths'].cumsum()
            df1['season_headshots'] = df.groupby('season')['headshots'].cumsum()
            df1['season_headshotPct'] = df1.season_headshots / df1.season_kills
            df1['season_kd'] = df1.season_kills / df1.season_deaths


            df1['season_gulagKills'] = df.groupby('season')['gulagKills'].cumsum()
            df1['season_gulagDeaths'] = df.groupby('season')['gulagDeaths'].cumsum()
            df1['season_gulag_winPct'] = df1.season_gulagKills / (df1.season_gulagKills + df1.season_gulagDeaths)
        df1[col_name] = df1['season_kd'].rolling(50).mean().fillna(df1["season_kd"])
        # df["COL3"] = df["COL1"].fillna(df["COL2"])
        dfs.append(df1)

    # building up finished DataFrame
    df = pd.concat(dfs,ignore_index=True)
    return df

    
def test_user_files(pewpers):

    #Import CSV into Pandas DF
    directory = r'./all_matches'
    df = pd.read_csv (r'./user_files/test_DirtyUndies.csv')

    print(df)

    df = df.sort_values(by=['start'])
    df = df.set_index('matchID',drop=False)
    df.reset_index(inplace=True, drop=True)

    #create cumulative totals
    
    df['total_kills'] = df.kills.cumsum()
    df['total_deaths'] = df.deaths.cumsum()
    df['total_headshots'] = df.headshots.cumsum()
    df['total_headshotPct'] = df.total_headshots / df.total_kills
    df['total_kd'] = df.total_kills / df.total_deaths
    df['kd_last50'] = df['total_kd'].rolling(50).mean()

    df['total_gulagKills'] = df.gulagKills.cumsum()
    df['total_gulagDeaths'] = df.gulagDeaths.cumsum()
    df['total_gulag_winPct'] = df.total_gulagKills / (df.total_gulagKills + df.total_gulagDeaths)
    df['gulag_last50'] = df['total_gulag_winPct'].rolling(50).mean()

    seasons = ['mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']

    dfs =[]
    for s in seasons:
        col_name = str(s) + '_kd_last50'
        print(col_name)
        df1 = df[df['season'] == s]
        print(len(df1))
        if (len(df1) == 0):
            
            df1['season_kills'] = 0
            df1['season_deaths'] = 0
            df['season_headshots'] = 0
            df['season_headshotPct'] = 0
            df1['season_kd'] = 0
            df1['season_gulagKills'] = 0
            df1['season_gulagDeaths'] = 0
            df1['season_gulag_winPct'] = 0

        else:
            df1['season_kills'] = df.groupby('season')['kills'].cumsum()
            df1['season_deaths'] = df.groupby('season')['deaths'].cumsum()
            df1['season_headshots'] = df.groupby('season')['headshots'].cumsum()
            df1['season_headshotPct'] = df1.season_headshots / df1.season_kills
            df1['season_kd'] = df1.season_kills / df1.season_deaths


            df1['season_gulagKills'] = df.groupby('season')['gulagKills'].cumsum()
            df1['season_gulagDeaths'] = df.groupby('season')['gulagDeaths'].cumsum()
            df1['season_gulag_winPct'] = df1.season_gulagKills / (df1.season_gulagKills + df1.season_gulagDeaths)
        df1[col_name] = df1['season_kd'].rolling(50).mean()
        dfs.append(df1)

    # building up finished DataFrame
    df = pd.concat(dfs,ignore_index=True)


    print('df')
    print(df)

    file_name = str('user_files/test2_'+df.iloc[0]['user']+ '.csv')
    print('Create file: ' + file_name)
    df.to_csv(file_name, index=False)



def main():
        pewpers = ['DirtyUndies', 'cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator', 'TD994', 'MkeBeers54']

        # Order
        # 1. run index.js to get all matches, followed by all_match_data csv file
        # 2. create
        #create_full_agg(pewpers)
        create_user_files(pewpers)
        #test_user_files(pewpers)

main()