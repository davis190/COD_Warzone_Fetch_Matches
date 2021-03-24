import pandas as pd
import numpy as np
# import pandasql as ps
import json
import csv
import os
from functools import reduce
import inspect, re
import datetime
from datetime import timedelta, date
import time

#Takes a master list of all matches for all users
#Creates separate DF for each user
#Creates a user specific list of games with teammates columns

def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)


def my_ceil(a, precision=2):
    return np.round(a + 0.5 * 10**(-precision), precision)

def my_floor(a, precision=2):
    return np.round(a - 0.5 * 10**(-precision), precision)

def create_full_agg(pewpers):

    field_names = ["matchID", "user", "mode","br_stats", "start", "end",
        "kills",
        "deaths",
        "teamPlacement",
        "headshots",
        "assists",
        "kdRatio",
        "gulagKills",
        "gulagDeaths",
        "damageDone",
        "damageTaken",
        "objectiveTeamWiped","objectiveReviver",
        "wallBangs",
        "executions",
        "longestStreak",
        "distanceTraveled",
        "percentTimeMoving",
        "timePlayed",
        "teamSurvivalTime",
        "score",
        "scorePerMinute",
        "matchXp",
        "scoreXp",
        "totalXp",
        "medalXp",
        "challengeXp",
        "bonusXp",
        "miscXp",
        "rank",
        "nearmisses",
        "team_rank",
        "objectiveMunitionsBoxTeammateUsed",
        "objectiveBrMissionPickupTablet",
        "objectiveBrKioskBuy","objectiveBrCacheOpen",
        "objectiveBrDownEnemyCircle1","objectiveBrDownEnemyCircle2","objectiveBrDownEnemyCircle3","objectiveBrDownEnemyCircle4", "objectiveBrDownEnemyCircle5","objectiveBrDownEnemyCircle6",
        "objectiveLastStandKill",
        "objectivePerkMarkedTarget",
        "objectiveDestroyedEquipment",
        "objectiveTrophyDefense",
        "objectiveAssistDecoy",
        "objectiveEmpedPlayer",
        "objectiveBinocularsMarked", "objectiveShieldDamage", "objectiveBrC130BoxOpen",
        "objectiveDestroyedVehicleHeavy", "objectiveMedalScoreKillSsManualTurret", "objectiveMedalScoreKillSsRadarDrone",
        "objectiveDestroyedVehicleLight","objectiveMedalScoreSsKillTomaStrike", "objectiveDestroyedVehicleMedium", 
        "objectivePlunderCashBloodMoney", "objectiveMedalScoreSsKillPrecisionAirstrike", "objectiveManualFlareMissileRedirect",
        "objectiveMedalScoreSsKillJuggernaut", "objectiveMedalScoreSsKillManualTurret", 'objectiveBrLootChopperBoxOpen', "objectiveWeaponDropTeammateUsed",
        "primaryWeapon1", "secondaryWeapon1", "lethal1", "tactical1",
        "primaryWeapon2", "secondaryWeapon2", "lethal2", "tactical2",
        "primaryWeapon3", "secondaryWeapon3", "lethal3", "tactical3",
        "primaryWeapon4", "secondaryWeapon4", "lethal4", "tactical4",
        "primaryWeapon5", "secondaryWeapon5", "lethal5", "tactical5",
        "primaryWeapon6", "secondaryWeapon6", "lethal6", "tactical6"
        ]

    # Match Types not to add to stats
    filter_matches = ['br_dmz_plnbld',
                'br_dmz_plndcndy',
                'br_dmz_plndtrios',
                'br_dmz_plndval1',
                'br_dmz_plunquad',
                'brtdm_rmbl',
                'br_kingslayer_kingsltrios'
    ]

    # create list br_stats == False
    other_modes = [
        'br_mini_rebirth_mini_royale_duos',
        'br_mini_rebirth_mini_royale_solo',
        'br_rebirth_rbrthtrios',
        'br_truckwar_trwarsquads',
        'br_zxp_zmbroy',
        'br_rebirth_rbrthtrios',
        'br_rebirth_rbrthquad'
    ]

    # removing 'br_mini_miniroyale' from other_modes

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
        filecount = 0
        for filename in os.listdir(directory):
            fullPath = os.path.join(directory, filename)
            
            if filename.endswith(".json") :
                with open(fullPath) as f:
                    match = json.load(f)

            players = match['allPlayers']

            # print(filename)

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
                            if mode in other_modes:
                                entry['br_stats'] = False
                            else:
                                entry['br_stats'] = True
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

                            w = 1
                            for z in p['player']['loadout']:                      
                                entry['primaryWeapon' + str(w)] = z['primaryWeapon']['name']
                                entry['secondaryWeapon' + str(w)] = z['secondaryWeapon']['name']
                                entry['tactical' + str(w)] = z['tactical']['name']
                                entry['lethal' + str(w)] = z['lethal']['name']
                                w = w + 1
                            writer.writerow(entry)

                    else:
                        # move plunder games to new location
                        new_path = os.path.join('/Users/cott/Repos/COD_Warzone_Fetch_Matches/filter_out_matches/',filename)
                        os.rename(fullPath, new_path)
                        filecount = filecount + 1

                except Exception as e:
                    #print(fullPath)
                    #print('EXCEPTION:', e)
                    if filename not in bad_files:
                        bad_files.append(filename)
    print('Files moved to filtered folder:', filecount)
    print('Bad Files:', bad_files)



def create_user_files(pewpers):

    #Import CSV into Pandas DF
    df = pd.read_csv (r'all_match_data.csv')

    df['matchID'] = df['matchID'].astype(str) + "_"

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
        user_df = user_df[user_df['percentTimeMoving'] > 0 ]

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
    df['total_kd_up'] = df['total_kd'].apply(lambda x: kd_gap(x,'up'))
    df['total_kd_down'] = df['total_kd'].apply(lambda x: kd_gap(x,'down'))
    df['kills_to_go_up'] = (df['total_kd_up'] * df['total_deaths']) - df['total_kills']
    df['deaths_to_go_down'] = (df['total_kills'] / df['total_kd_down']) - df['total_deaths']

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

    
def test(pewpers):

    field_names = ["matchID", "user", "mode","start", "end",
        "kills",
        "deaths",
        "teamPlacement",
        "headshots",
        "assists",
        "kdRatio",
        "gulagKills",
        "gulagDeaths",
        "damageDone",
        "damageTaken",
        "medalXp",
        "objectiveTeamWiped",
        "matchXp",
        "scoreXp",
        "wallBangs",
        "score",
        "totalXp",
        "challengeXp",
        "rank",
        "scorePerMinute",
        "distanceTraveled",
        "teamSurvivalTime",
        "objectiveMunitionsBoxTeammateUsed",
        "objectiveBrDownEnemyCircle1","objectiveBrDownEnemyCircle2","objectiveBrDownEnemyCircle3","objectiveBrDownEnemyCircle4", "objectiveBrDownEnemyCircle5","objectiveBrDownEnemyCircle6",
        "objectiveBrMissionPickupTablet",
        "bonusXp",
        "objectiveBrKioskBuy",
        "timePlayed",
        "executions",
        "nearmisses",
        "objectiveBrCacheOpen",
        "percentTimeMoving",
        "miscXp",
        "longestStreak",
        "team_rank",
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
        "objectiveMedalScoreSsKillJuggernaut", "objectiveMedalScoreSsKillManualTurret", 'objectiveBrLootChopperBoxOpen', "objectiveWeaponDropTeammateUsed",
        "primaryWeapon1", "secondaryWeapon1", "lethal1", "tactical1",
        "primaryWeapon2", "secondaryWeapon2", "lethal2", "tactical2",
        "primaryWeapon3", "secondaryWeapon3", "lethal3", "tactical3",
        "primaryWeapon4", "secondaryWeapon4", "lethal4", "tactical4",
        "primaryWeapon5", "secondaryWeapon5", "lethal5", "tactical5",
        "primaryWeapon6", "secondaryWeapon6", "lethal6", "tactical6"
        ]

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
    with open('test_all_match_data.csv', 'w') as csvfile:
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

                            w = 1
                            for z in p['player']['loadout']:                                
                                entry['primaryWeapon' + str(w)] = z['primaryWeapon']['name']
                                entry['secondaryWeapon' + str(w)] = z['secondaryWeapon']['name']
                                entry['tactical' + str(w)] = z['tactical']['name']
                                entry['lethal' + str(w)] = z['lethal']['name']
                                w = w + 1
                            #     k = k  + 1
                                # print(key, '->', p['playerStats'][key])
                                # stats.append(p['playerStats'][key])
                            writer.writerow(entry)

                except Exception as e:
                    print('exception')
                    print(fullPath)
                    print(e)
                    if filename not in bad_files:
                        bad_files.append(filename)
    print(bad_files)

def kd_gap(kd, direction):

    base = 0.005

    
    #print(base)
    nearest_multiple = base * round(kd/base)
    #print('nearest_multiple', nearest_multiple)

    #remove integer and jsut compare decimals
    dec = round(kd,1)
    #print(dec)
    dec = kd - dec
    #print(dec)

    if (dec < .003):
        #print('a')
        kd_up = nearest_multiple + 0.005
        kd_down = nearest_multiple - 0.006
    elif (dec > .003) and (dec < .0049):
        #print('b')
        kd_up = nearest_multiple
        kd_down = nearest_multiple - 0.011
    elif (dec >= .0049) and (dec < .0079):
        #print('c')
        kd_up = nearest_multiple + .01
        kd_down = nearest_multiple - .001
    elif (dec > .0079):
        #print('d')
        kd_up = nearest_multiple + 0.005
        kd_down = nearest_multiple - 0.006
    # print('kd_up', kd_up)
    # print('kd_down', kd_down)
    # print('--------')

    if direction == 'up':
        return kd_up
    if direction == 'down':
        return kd_down


def season_totals(pewpers, seasons): #sesaon_dashboard


    # seasons = ['all', 'mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']
    for s in seasons:
        df_list =[]
        for p in pewpers:
            file_name = "user_files/"+ p+".csv"
            df = pd.read_csv (file_name)

            season_df = df.groupby(['season']).count()


            games_list = []
            wins_list = []
            win_pct= []
            kills_list = []
            deaths_list = []
            kd_list = []
            # downs_list = []
            top5_list =[]
            top10_list = []
            top25_list = []
            top5_pct = []
            top10_pct = []
            top25_pct = []

            if s == 'all':
                #Get Games count
                games = (df.loc[ (df['br_stats'] == True),'matchID']).count()
                games_list.append(games)

                #Get Wins by Season
                wins = (df.loc[ (df['br_stats'] == True) & (df['teamPlacement'] == 1),'teamPlacement']).count()
                wins_list.append(wins)

                #win_pct
                win_p = round(wins / games * 100,1)
                win_pct.append(win_p)

                #Kills by Season
                kills = (df.loc[ (df['br_stats'] == True),'kills']).sum()
                kills_list.append(kills)
                
                #Deaths by Season
                deaths = (df.loc[ (df['br_stats'] == True),'deaths']).sum()
                # print(deaths)
                deaths_list.append(deaths)
                
                # #KD by Season
                kd = round(kills /  deaths,2)
                # print(kd)
                kd_list.append(kd)

                #downs by Season
                # downs = (df.loc[(df['season']== s),'downs']).sum()
                # downs_list.append(downs)

                #downs by Season
                top5 = (df.loc[ (df['br_stats'] == True) & (df['teamPlacement'] < 6),'teamPlacement']).count()
                top5_list.append(top5)

                #top5_pct
                top5_p = round(top5 / games * 100,1)
                top5_pct.append(top5_p)

                #downs by Season
                top10 = (df.loc[ (df['br_stats'] == True) & (df['teamPlacement'] < 11),'teamPlacement']).count()
                top10_list.append(top10)

                #top10_pct
                top10_p = round(top10 / games * 100,1)
                top10_pct.append(top10_p)

                #downs by Season
                top25 = (df.loc[ (df['br_stats'] == True) & (df['teamPlacement'] < 26),'teamPlacement']).count()
                top25_list.append(top25)

                #top25_pct
                top25_p = round(top25 / games * 100,1)
                top25_pct.append(top25_p)
            else:

                #Get Games count
                games = (df.loc[(df['season']== s) & (df['br_stats'] == True),'matchID']).count()
                games_list.append(games)

                #Get Wins by Season
                wins = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] == 1),'teamPlacement']).count()
                wins_list.append(wins)

                #win_pct
                win_p = round(wins / games * 100,1)
                win_pct.append(win_p)

                #Kills by Season
                kills = (df.loc[(df['season']== s) & (df['br_stats'] == True),'kills']).sum()
                kills_list.append(kills)
                
                #Deaths by Season
                deaths = (df.loc[(df['season']== s) & (df['br_stats'] == True),'deaths']).sum()
                # print(deaths)
                deaths_list.append(deaths)
                
                # #KD by Season
                kd = round(kills /  deaths,2)
                # print(kd)
                kd_list.append(kd)

                #downs by Season
                # downs = (df.loc[(df['season']== s),'downs']).sum()
                # downs_list.append(downs)

                #downs by Season
                top5 = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 6),'teamPlacement']).count()
                top5_list.append(top5)

                #top5_pct
                top5_p = round(top5 / games * 100,1)
                top5_pct.append(top5_p)

                #downs by Season
                top10 = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 11),'teamPlacement']).count()
                top10_list.append(top10)

                #top10_pct
                top10_p = round(top10 / games * 100,1)
                top10_pct.append(top10_p)

                #downs by Season
                top25 = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 26),'teamPlacement']).count()
                top25_list.append(top25)

                #top25_pct
                top25_p = round(top25 / games * 100,1)
                top25_pct.append(top25_p)

            d = {
                'user': p,
                'games': games_list, 
                'wins': wins_list, 
                'win_pct': win_pct,
                'kills': kills_list, 
                'deaths': deaths_list, 
                'kd': kd_list,
                # 'downs': downs_list,
                'top5': top5_list,
                'top5_pct': top5_pct,
                'top10': top10_list,
                'top10_pct': top10_pct,
                'top25': top25_list,
                'top25_pct': top25_pct,
            }
            user_df = pd.DataFrame(data=d)
            # print(user_df)
            df_list.append(user_df)
        merged = pd.concat(df_list)
    
        # print(merged)

        file_name = str('MWBattleData/season_totals/'+s+'.csv')
        print('Create file: ' + file_name)
        merged.to_csv(file_name, index=False)

def daily_totals(pewpers): #daily_totals

    current_date = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    today = current_date.date()
    tomorrow = today + timedelta(days = 1)
    yest = today - timedelta(days = 1)
    # print('current_date', current_date)

    print(today)
    print(tomorrow)
    print(yest)


    # unix time for today and yesterday
    t = time.mktime(today.timetuple())
    tom = time.mktime(tomorrow.timetuple())
    y =  time.mktime(yest.timetuple())
    print(int(t), int(tom), int(y))

    df_list =[]
    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        games_list = []
        wins_list = []
        kills_list = []
        deaths_list = []
        kd_list = []
        top5_list =[]
        top10_list = []
        top25_list = []

        y_games_list = []
        y_wins_list = []
        y_kills_list = []
        y_deaths_list = []
        y_kd_list = []
        y_top5_list =[]
        y_top10_list = []
        y_top25_list = []


        #Get Games count
        games = (df.loc[(df['start'] > t) & (df['br_stats'] == True),'matchID']).count()
        games_list.append(games)

        #Get Wins by Season
        wins = (df.loc[(df['start'] > t) & (df['start'] < tom) & (df['br_stats'] == True) & (df['teamPlacement'] == 1),'teamPlacement']).count()
        wins_list.append(wins)

        #Kills by Season
        kills = (df.loc[ (df['start'] > t) & (df['start'] < tom) & (df['br_stats'] == True),'kills']).sum()
        kills_list.append(kills)
        
        #Deaths by Season
        deaths = (df.loc[ (df['start'] > t) & (df['start'] < tom) & (df['br_stats'] == True),'deaths']).sum()
        # print(deaths)
        deaths_list.append(deaths)
        
        # #KD by Season
        kd = round(kills /  deaths,2)
        # print(kd)
        kd_list.append(kd)


        #downs by Season
        top5 = (df.loc[ (df['start'] > t) & (df['start'] < tom) & (df['br_stats'] == True) & (df['teamPlacement'] < 6),'teamPlacement']).count()
        top5_list.append(top5)


        #downs by Season
        top10 = (df.loc[ (df['start'] > t) & (df['start'] < tom) & (df['br_stats'] == True) & (df['teamPlacement'] < 11),'teamPlacement']).count()
        top10_list.append(top10)


        #downs by Season
        top25 = (df.loc[ (df['start'] > t) & (df['start'] < tom) & (df['br_stats'] == True) & (df['teamPlacement'] < 26),'teamPlacement']).count()
        top25_list.append(top25)

        # YESTERDAY

        #Get Games count
        y_games = (df.loc[(df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True),'matchID']).count()
        y_games_list.append(y_games)

        #Get Wins by Season
        y_wins = (df.loc[(df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True) & (df['teamPlacement'] == 1),'teamPlacement']).count()
        y_wins_list.append(y_wins)

        #Kills by Season
        y_kills = (df.loc[ (df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True),'kills']).sum()
        y_kills_list.append(y_kills)
        
        #Deaths by Season
        y_deaths = (df.loc[ (df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True),'deaths']).sum()
        # print(deaths)
        y_deaths_list.append(y_deaths)
        
        # #KD by Season
        y_kd = round(y_kills /  y_deaths,2)
        # print(kd)
        y_kd_list.append(y_kd)


        #downs by Season
        y_top5 = (df.loc[ (df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True) & (df['teamPlacement'] < 6),'teamPlacement']).count()
        y_top5_list.append(y_top5)


        #downs by Season
        y_top10 = (df.loc[ (df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True) & (df['teamPlacement'] < 11),'teamPlacement']).count()
        y_top10_list.append(y_top10)


        #downs by Season
        y_top25 = (df.loc[ (df['start'] > y) & (df['start'] < t) & (df['br_stats'] == True) & (df['teamPlacement'] < 26),'teamPlacement']).count()
        y_top25_list.append(y_top25)


        d = {
            'user': p,
            'games': games_list, 
            'wins': wins_list, 
            'kills': kills_list, 
            'deaths': deaths_list, 
            'kd': kd_list,
            'top5': top5_list,
            'top10': top10_list,
            'top25': top25_list,
            'y_games': y_games_list, 
            'y_wins': y_wins_list, 
            'y_kills': y_kills_list, 
            'y_deaths': y_deaths_list, 
            'y_kd': y_kd_list,
            'y_top5': y_top5_list,
            'y_top10': y_top10_list,
            'y_top25': y_top25_list,

        }
        user_df = pd.DataFrame(data=d)
        df_list.append(user_df)
    merged = pd.concat(df_list)

    print(merged)

    file_name = str('MWBattleData/daily_totals/'+str(today)+'.csv')
    print('Create file: ' + file_name)
    merged.to_csv(file_name, index=False)

def daily_games(pewpers): #daily_totals

    current_date = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    today = current_date.date()
    tomorrow = today + timedelta(days = 1)
    yest = today - timedelta(days = 1)
    # print('current_date', current_date)

    print(today)
    print(tomorrow)
    print(yest)


    # unix time for today and yesterday
    t = time.mktime(today.timetuple())
    tom = time.mktime(tomorrow.timetuple())
    y =  time.mktime(yest.timetuple())
    print(int(t), int(tom), int(y))

    df_list =[]
    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        games_list = []


        #Get Games count
        user_df = df.loc[(df['start'] > y)]

        df_list.append(user_df)
    merged = pd.concat(df_list)

    #rename mode col
    merged['mode'].mask(merged['mode'] == 'br_brtrios', 'Trios', inplace=True)
    merged['mode'].mask(merged['mode'] == 'br_brsolo', 'Solo', inplace=True)
    merged['mode'].mask(merged['mode'] == 'br_brduos', 'Duos', inplace=True)
    merged['mode'].mask(merged['mode'] == 'br_brquads', 'Quads', inplace=True)

    merged['gulagDeaths'].mask(merged['gulagDeaths'] >= 1, 1, inplace=True)


    merged = merged.sort_values(by=['start'])
    merged = merged[['matchID', 'start', 'user', 'mode', 'teamPlacement', 'kills', 'deaths', 'kdRatio', 'assists', 'downs', 'damageDone', 'damageTaken', 'gulagKills', 'gulagDeaths', 'headshots', 'objectiveTeamWiped', 'percentTimeMoving', 'objectiveReviver']]
    #convert to timestamp
    merged['start']= pd.to_datetime(merged['start'],unit='s')
    # merged.start = merged.start.dt.tz_localize('UTC').dt.tz_convert('America/Chicago')

    merged.start = merged.start - pd.Timedelta('05:00:00')

    merged['kdRatio'] = round(merged['kdRatio'],2)
    merged.downs = merged.downs.astype(int)
    merged.damageDone = merged.damageDone.astype(int)
    merged.damageTaken = merged.damageTaken.astype(int)
    merged.gulagKills = merged.gulagKills.astype(int)
    merged.gulagDeaths = merged.gulagDeaths.astype(int)
    merged.headshots = merged.headshots.astype(int)
    merged.objectiveTeamWiped = merged.objectiveTeamWiped.fillna(0)
    merged.objectiveReviver = merged.objectiveReviver.fillna(0)
    merged.objectiveTeamWiped = merged.objectiveTeamWiped.astype(int)
    merged.percentTimeMoving = merged.percentTimeMoving.astype(int)
    merged.objectiveReviver = merged.objectiveReviver.astype(int)
    merged.teamPlacement = merged.teamPlacement.astype(int)

    # merged['damageDone'] = int(merged['damageDone'])
    # merged['damageTaken'] = int(merged['damageTaken'])
    # merged['gulagKills'] = int(merged['gulagKills'])
    # merged['gulagDeaths'] = int(merged['gulagDeaths'])
    # merged['headshots'] = int(merged['headshots'])
    # merged['objectiveTeamWiped'] = int(merged['objectiveTeamWiped'])
    # merged['percentTimeMoving'] = round(merged['percentTimeMoving'],0)

    print(merged)   
    file_name = str('MWBattleData/daily_games/'+str(today)+'.csv')
    print('Create file: ' + file_name)
    merged.to_csv(file_name, index=False)

def weekly_kd_chart(pewpers): #daily_totals

    current_date = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    today = current_date.date()
    tomorrow = today + timedelta(days = 1)
    yest = today - timedelta(days = 1)
    last_wk = today - timedelta(days = 10)
    # print('current_date', current_date)

    # print(today)
    # print(tomorrow)
    # print(yest)


    # unix time for today and yesterday
    t = time.mktime(today.timetuple())
    tom = time.mktime(tomorrow.timetuple())
    # y =  time.mktime(yest.timetuple())
    wk = time.mktime(last_wk.timetuple())
    # print(int(t), int(tom), int(wk))

    df_list =[]
    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        games_list = []


        #Get Games count
        user_df = df.loc[(df['start'] > wk)]

        df_list.append(user_df)
        merged = pd.concat(df_list)

        #rename mode col
        merged['mode'].mask(merged['mode'] == 'br_brtrios', 'Trios', inplace=True)
        merged['mode'].mask(merged['mode'] == 'br_brsolo', 'Solo', inplace=True)
        merged['mode'].mask(merged['mode'] == 'br_brduos', 'Duos', inplace=True)
        merged['mode'].mask(merged['mode'] == 'br_brquads', 'Quads', inplace=True)

        merged = merged.sort_values(by=['start'])
        merged = merged[['start', 'kills', 'deaths']]
        #convert to timestamp
        merged['start']= pd.to_datetime(merged['start'],unit='s')
        # merged.start = merged.start.dt.tz_localize('UTC').dt.tz_convert('America/Chicago')

        merged.start = merged.start - pd.Timedelta('05:00:00')

        merged = merged.set_index('start').groupby(pd.Grouper(freq='D')).sum()


        print(merged)   

        out_dir ='./MWBattleData/chartWeekKd/'
        # try:
        #     os.mkdir(out_dir)
        # except:
        #     print(out_dir, 'previously created')
        file_name = out_dir +  str(p)+'.csv'
        print('Create file: ' + file_name)
        merged.to_csv(file_name, index=True)


def season_stats(pewpers, seasons):

    # seasons = ['mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2', 'all']

    for s in seasons:
        df_list =[]
        for p in pewpers:
            file_name = "user_files/"+ p+".csv"
            df = pd.read_csv (file_name)

            # season_df = df.groupby(['season']).count()

            seasons = ['all']#'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']
            
            avg_fin_ls = []
            mx_kills_ls = []
            kills_list = []
            deaths_list = []
            ass_ls =[]
            downs_list = []
            exec_ls =[]
            head_ls= []
            headpct_ls= []
            gulag_w_ls = []
            gulag_l_ls =[]
            gulag_pct_ls =[]

            # games_list = []
            # wins_list = []
            # win_pct= []
            # kills_list = []

            # kd_list = []
            
            # top5_list =[]
            # top10_list = []
            # top25_list = []
            # top5_pct = []
            # top10_pct = []
            # top25_pct = []
            # for s in seasons:

            if s == 'all':
                #Get Games count
                games = (df.loc[(df['br_stats'] == True),'matchID']).count()
                #Kills by Season
                kills = (df.loc[(df['br_stats'] == True),'kills']).sum()
                #Deaths by Season
                deaths = (df.loc[(df['br_stats'] == True),'deaths']).sum()

                #Get average finish
                avFin = (df.loc[(df['br_stats'] == True),'teamPlacement']).mean()
                avFin = round(avFin,1)
                avg_fin_ls.append(avFin)

                #Get Max Kills by Season
                mxk = (df.loc[(df['br_stats'] == True),'kills']).max()
                mx_kills_ls.append(mxk)

                #kills/gm
                kills_gm  = round(kills / games,2)
                kills_list.append(kills_gm)

                #deaths/gm
                deaths_gm  = round(deaths / games,2)
                deaths_list.append(deaths_gm)

                #assists
                assists = (df.loc[(df['br_stats'] == True),'assists']).sum()
                ass_ls.append(assists)

                #downs
                downs = (df.loc[(df['br_stats'] == True),'downs']).sum()
                downs = int(downs)
                downs_list.append(downs)

                #exec
                execs = (df.loc[(df['br_stats'] == True),'executions']).sum()
                exec_ls.append(execs)

                #headshot
                headshots = (df.loc[(df['br_stats'] == True),'headshots']).sum()
                headshot = int(headshots)
                head_ls.append(headshots)

                #headshot %
                h_pct = round(headshots / kills * 100, 1)
                headpct_ls.append(h_pct)

                #gulag w
                gw = (df.loc[(df['br_stats'] == True),'gulagKills']).sum()
                gw = int(gw)
                gulag_w_ls.append(gw)


                #gulag L (count because can be more than 1)
                gl = (df.loc[(df['br_stats'] == True),'gulagDeaths']).count()
                gl= int(gl)
                gulag_l_ls.append(gl)

                #gulag pct
                try:
                    gp = round(gw / (gw+gl) * 100, 1)
                except:
                    gp = 0.0
                gulag_pct_ls.append(gp)
            else:

                #Get Games count
                games = (df.loc[(df['season']== s) & (df['br_stats'] == True),'matchID']).count()
                #Kills by Season
                kills = (df.loc[(df['season']== s) & (df['br_stats'] == True),'kills']).sum()
                #Deaths by Season
                deaths = (df.loc[(df['season']== s) & (df['br_stats'] == True),'deaths']).sum()

                #Get average finish
                avFin = (df.loc[(df['season']== s) & (df['br_stats'] == True),'teamPlacement']).mean()
                avFin = round(avFin,1)
                avg_fin_ls.append(avFin)

                #Get Max Kills by Season
                mxk = (df.loc[(df['season']== s) & (df['br_stats'] == True),'kills']).max()
                mx_kills_ls.append(mxk)

                #kills/gm
                kills_gm  = round(kills / games,2)
                kills_list.append(kills_gm)

                #deaths/gm
                deaths_gm  = round(deaths / games,2)
                deaths_list.append(deaths_gm)

                #assists
                assists = (df.loc[(df['season']== s) & (df['br_stats'] == True),'assists']).sum()
                ass_ls.append(assists)

                #downs
                downs = (df.loc[(df['season']== s) & (df['br_stats'] == True),'downs']).sum()
                downs = int(downs)
                downs_list.append(downs)

                #exec
                execs = (df.loc[(df['season']== s) & (df['br_stats'] == True),'executions']).sum()
                exec_ls.append(execs)

                #headshot
                headshots = (df.loc[(df['season']== s) & (df['br_stats'] == True),'headshots']).sum()
                headshots = round(int(headshots),0)
                head_ls.append(headshots)

                #headshot %
                h_pct = round(headshots / kills * 100, 1)
                headpct_ls.append(h_pct)

                #gulag w
                gw = (df.loc[(df['season']== s) & (df['br_stats'] == True),'gulagKills']).sum()
                gw = int(gw)
                gulag_w_ls.append(gw)


                #gulag L
                gl = (df.loc[(df['season']== s) & (df['br_stats'] == True),'gulagDeaths']).sum()
                gl= int(gl)
                gulag_l_ls.append(gl)

                #gulag pct
                try:
                    gp = round(gw / (gw+gl) * 100, 1)
                except:
                    gp = 0.0
                gulag_pct_ls.append(gp)

            d = {
                'user' : p, 
                'avg_finish': avg_fin_ls,
                'max_kills': mx_kills_ls, 
                'kills_gm': kills_list, 
                'deaths_gm': deaths_list, 
                'assists': ass_ls,
                'downs': downs_list,
                'executions': exec_ls, 
                'headshots': head_ls, 
                'headshot_pct': headpct_ls,
                'gulag_wins': gulag_w_ls,
                'gulag_deaths': gulag_l_ls,
                'gulag_pct': gulag_pct_ls,
            }
            user_df = pd.DataFrame(data=d)
            # print(user_df)
            df_list.append(user_df)
        merged = pd.concat(df_list)
    
        # print(merged))

        file_name = str('MWBattleData/season_stats/'+s+'.csv')
        print('Create file: ' + file_name)
        merged.to_csv(file_name, index=False)

#copy this for user_mode_totals
#and user_teammate_totals
def user_season_totals(pewpers):


    df_list =[]
    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        seasons = ['mw_1','mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']
        games_list = []
        wins_list = []
        win_pct= []
        kills_list = []
        deaths_list = []
        kd_list = []
        # downs_list = []
        top5_list =[]
        top10_list = []
        top25_list = []
        top5_pct = []
        top10_pct = []
        top25_pct = []
        s_list = []
        df_list= []
        o_ls=[]
        order = [1, 2, 3, 4, 5, 6, 7, 8]
        i = 0
        for s in seasons:
            o_ls.append(order[i])
            i = i + 1
            #Get Games count
            games = (df.loc[(df['season']== s) & (df['br_stats'] == True),'matchID']).count()
            games_list.append(games)

            #Get Wins by Season
            wins = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] == 1),'teamPlacement']).count()
            wins_list.append(wins)

            #win_pct
            win_p = round(wins / games * 100,1)
            win_pct.append(win_p)

            #Kills by Season
            kills = (df.loc[(df['season']== s) & (df['br_stats'] == True),'kills']).sum()
            kills_list.append(kills)
            
            #Deaths by Season
            deaths = (df.loc[(df['season']== s) & (df['br_stats'] == True),'deaths']).sum()
            # print(deaths)
            deaths_list.append(deaths)
            
            # #KD by Season
            kd = round(kills /  deaths,2)
            # print(kd)
            kd_list.append(kd)

            #downs by Season
            # downs = (df.loc[(df['season']== s),'downs']).sum()
            # downs_list.append(downs)

            #downs by Season
            top5 = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 6),'teamPlacement']).count()
            top5_list.append(top5)

            #top5_pct
            top5_p = round(top5 / games * 100,1)
            top5_pct.append(top5_p)

            #downs by Season
            top10 = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 11),'teamPlacement']).count()
            top10_list.append(top10)

            #top10_pct
            top10_p = round(top10 / games * 100,1)
            top10_pct.append(top10_p)

            #downs by Season
            top25 = (df.loc[(df['season']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 26),'teamPlacement']).count()
            top25_list.append(top25)

            #top25_pct
            top25_p = round(top25 / games * 100,1)
            top25_pct.append(top25_p)
            s_list.append(s)

        d = {
            'order': o_ls, 
            'season': s_list,
            'games': games_list, 
            'wins': wins_list, 
            'win_pct': win_pct,
            'kills': kills_list, 
            'deaths': deaths_list, 
            'kd': kd_list,
            # 'downs': downs_list,
            'top5': top5_list,
            'top5_pct': top5_pct,
            'top10': top10_list,
            'top10_pct': top10_pct,
            'top25': top25_list,
            'top25_pct': top25_pct,
        }
        user_df = pd.DataFrame(data=d)
        # print(user_df)
        df_list.append(user_df)
        merged = pd.concat(df_list)
        
        # print(merged))

        file_name = str('MWBattleData/user_season_totals/'+p+'.csv')
        print('Create file: ' + file_name)
        merged.to_csv(file_name, index=False)


def user_mode_totals(pewpers):


    df_list =[]
    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        season_df = df.groupby(['season']).count()

        # seasons = ['mw_1','mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']
        modes = ['br_brsolo', 'br_brduos', 'br_brtrios', 'br_brquads']
        games_list = []
        wins_list = []
        win_pct= []
        kills_list = []
        deaths_list = []
        kd_list = []
        # downs_list = []
        top5_list =[]
        top10_list = []
        top25_list = []
        top5_pct = []
        top10_pct = []
        top25_pct = []
        s_list = []
        df_list= []
        avg_fin_ls =[]
        mx_kills_ls=[]
        kills_list_gm=[]
        deaths_list_gm=[]
        head_ls=[]

        for s in modes:

            #Get Games count
            games = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'matchID']).count()
            games_list.append(games)

            #Get Wins by Season
            wins = (df.loc[(df['mode']== s) & (df['br_stats'] == True) & (df['teamPlacement'] == 1),'teamPlacement']).count()
            wins_list.append(wins)

            #win_pct
            win_p = round(wins / games * 100,1)
            win_pct.append(win_p)

            #Kills by Season
            kills = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'kills']).sum()
            kills_list.append(kills)
            
            #Deaths by Season
            deaths = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'deaths']).sum()
            # print(deaths)
            deaths_list.append(deaths)
            
            # #KD by Season
            kd = round(kills /  deaths,2)
            # print(kd)
            kd_list.append(kd)

            #downs by Season
            # downs = (df.loc[(df['season']== s),'downs']).sum()
            # downs_list.append(downs)

            #downs by Season
            top5 = (df.loc[(df['mode']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 6),'teamPlacement']).count()
            top5_list.append(top5)

            #top5_pct
            top5_p = round(top5 / games * 100,1)
            top5_pct.append(top5_p)

            #downs by Season
            top10 = (df.loc[(df['mode']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 11),'teamPlacement']).count()
            top10_list.append(top10)

            #top10_pct
            top10_p = round(top10 / games * 100,1)
            top10_pct.append(top10_p)

            #downs by Season
            top25 = (df.loc[(df['mode']== s) & (df['br_stats'] == True) & (df['teamPlacement'] < 26),'teamPlacement']).count()
            top25_list.append(top25)

            #top25_pct
            top25_p = round(top25 / games * 100,1)
            top25_pct.append(top25_p)

            #Get average finish
            avFin = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'teamPlacement']).mean()
            avFin = round(avFin,1)
            avg_fin_ls.append(avFin)

            #Get Max Kills by mode
            mxk = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'kills']).max()
            mx_kills_ls.append(mxk)

            #kills/gm
            kills_gm  = round(kills / games,2)
            kills_list_gm.append(kills_gm)

            #deaths/gm
            deaths_gm  = round(deaths / games,2)
            deaths_list_gm.append(deaths_gm)

            #headshot
            headshots = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'headshots']).sum()
            headshots = round(int(headshots),1)
            head_ls.append(headshots)

            if s == 'br_brsolo':
                s = 'Solo'
            elif s == 'br_brduos':
                s = 'Duos'
            elif s == 'br_brtrios':
                s = 'Trios'
            elif  s == 'br_brquads':
                s = 'Quads'
            s_list.append(s)

        d = {
            'mode': s_list,
            'games': games_list, 
            'wins': wins_list, 
            'avg_fin':avg_fin_ls ,
            'win_pct': win_pct,
            'kills': kills_list, 
            'deaths': deaths_list, 
            'kd': kd_list,
            'max_kills':mx_kills_ls,
            'kill_gm':kills_list_gm,
            'deaths_gm':deaths_list_gm,
            'headshots':head_ls,
            'top5': top5_list,
            'top5_pct': top5_pct,
            'top10': top10_list,
            'top10_pct': top10_pct,
            'top25': top25_list,
            'top25_pct': top25_pct,
            
            
            }
        user_df = pd.DataFrame(data=d)
        # print(user_df)
        df_list.append(user_df)
        merged = pd.concat(df_list)
        
        # print(merged))

        file_name = str('MWBattleData/user_mode_totals/'+p+'.csv')
        print('Create file: ' + file_name)
        merged.to_csv(file_name, index=False)

def user_team_totals(pewpers):


    df_list =[]
    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        season_df = df.groupby(['season']).count()

        # seasons = ['mw_1','mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']
        # modes = ['br_brsolo', 'br_brduos', 'br_brtrios', 'br_brquads']
        games_list = []
        wins_list = []
        win_pct= []
        kills_list = []
        deaths_list = []
        kd_list = []
        # downs_list = []
        top5_list =[]
        top10_list = []
        top25_list = []
        top5_pct = []
        top10_pct = []
        top25_pct = []
        s_list = []
        df_list= []
        for s in pewpers:

            if s != p:
                # df2 = df.loc[((df['a'] > 1) & (df['b'] > 0)) | ((df['a'] < 1) & (df['c'] == 100))]

                #Get Games count
                games = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True)),'matchID']).count()
                # games = df2['matchID'].count()
                # games = (df.loc[(df['mode']== s) & (df['br_stats'] == True),'matchID']).count()
                games_list.append(games)

                #Get Wins by Season
                wins = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True) & (df['teamPlacement'] == 1)),'teamPlacement']).count()
                wins_list.append(wins)

                #win_pct
                win_p = round(wins / games * 100,1)
                win_pct.append(win_p)

                #Kills by Season
                kills = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True)),'kills']).sum()
                kills_list.append(kills)
                
                #Deaths by Season
                deaths = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True)),'deaths']).sum()
                # print(deaths)
                deaths_list.append(deaths)
                
                # #KD by Season
                kd = round(kills /  deaths,2)
                # print(kd)
                kd_list.append(kd)

                #downs by Season
                # downs = (df.loc[(df['season']== s),'downs']).sum()
                # downs_list.append(downs)

                #downs by Season
                top5 = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True) & (df['teamPlacement'] < 6)),'teamPlacement']).count()
                top5_list.append(top5)

                #top5_pct
                top5_p = round(top5 / games * 100,1)
                top5_pct.append(top5_p)

                #downs by Season
                top10 = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True) & (df['teamPlacement'] < 11)),'teamPlacement']).count()
                top10_list.append(top10)

                #top10_pct
                top10_p = round(top10 / games * 100,1)
                top10_pct.append(top10_p)

                #downs by Season
                top25 = (df.loc[(((df['teammate1']== s)| (df['teammate2']== s) | (df['teammate3']== s) | (df['teammate4']== s)) & (df['br_stats'] == True) & (df['teamPlacement'] < 26)),'teamPlacement']).count()
                top25_list.append(top25)

                #top25_pct
                top25_p = round(top25 / games * 100,1)
                top25_pct.append(top25_p)

                #append condition (teammate, sesaon, mode)
                s_list.append(s)

        d = {
            'teammate': s_list,
            'games': games_list, 
            'wins': wins_list, 
            'win_pct': win_pct,
            'kills': kills_list, 
            'deaths': deaths_list, 
            'kd': kd_list,
            # 'downs': downs_list,
            'top5': top5_list,
            'top5_pct': top5_pct,
            'top10': top10_list,
            'top10_pct': top10_pct,
            'top25': top25_list,
            'top25_pct': top25_pct,
        }
        user_df = pd.DataFrame(data=d)
        # print(user_df)
        df_list.append(user_df)
        merged = pd.concat(df_list)
        
        # print(merged))

        file_name = str('MWBattleData/user_team_totals/'+p+'.csv')
        print('Create file: ' + file_name)
        merged.to_csv(file_name, index=False)



def kd_chart(pewpers):

    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        # avg_fin_ls = []
        # mx_kills_ls = []
        # kills_list = []
        # deaths_list = []
        # ass_ls =[]
        # downs_list = []
        # exec_ls =[]
        # head_ls= []
        # headpct_ls= []
        # gulag_w_ls = []
        # gulag_l_ls =[]
        # gulag_pct_ls =[]

        # games_list = []
        # wins_list = []
        # win_pct= []
        # kills_list = []

        # kd_list = []
        
        # top5_list =[]
        # top10_list = []
        # top25_list = []
        # top5_pct = []
        # top10_pct = []
        # top25_pct = []

        match_ls= []
        kd_ls =[]
        kd_rolling =[]
        seasons = ['all', 'mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']

        for s in seasons:

            if s == 'all':
                #Get Games count
                games = (df.loc[(df['br_stats'] == True),['matchID','kills','deaths']])
            else:
                games = (df.loc[(df['season']== s) & (df['br_stats'] == True),['matchID','kills','deaths']])
            
            if len(games) > 1:
                
                games.reset_index(inplace=True)
                # games['kd'] = games.kills / games.deaths

                games['total_kills'] = games.kills.cumsum()
                games['total_deaths'] = games.deaths.cumsum()
                games['total_kd'] = round(games.total_kills / games.total_deaths,2)
                games['kd_rolling'] = round(games.kills.rolling(50).sum() / games.deaths.rolling(50).sum(),2)
                games['kd_rolling'].fillna(games['total_kd'], inplace=True)

                # games['kd_rolling'] = round(games['total_kd'].rolling(50).mean(),2)

                games.drop(['matchID', 'kills', 'deaths', 'total_kills', 'total_deaths'], axis=1, inplace=True)
                
                #reset index to begin with 1
                games['index'] = games['index'] - int(games.iloc[0]['index']-1)

                games.rename(columns={'index':'match'}, inplace=True)

            else:
                print('no matches for', p, s)

            # print(games)
            games = games.iloc[10:]
            # print(games)

            out_dir ='./MWBattleData/chartKd/{}'.format(p)
            try:
                os.mkdir(out_dir)
            except:
                print(out_dir, 'previously created')
            file_name = str(out_dir+'/'+s+'.csv')
            print('Create file: ' + file_name)
            games.to_csv(file_name, index=False)
            
            



            #     kills = (df.loc[(df['br_stats'] == True),['kills','deaths']])
            #     for k in kills:
            #         kd_ls.append(k)

            # print(match_ls)
            # print(kd_ls)
                # # deaths = (df.loc[(df['br_stats'] == True),'deaths'])
                # #Kills by Season
                


                # #Deaths by Season
                # deaths = (df.loc[(df['br_stats'] == True),'deaths']).sum()

                # #Get average finish
                # avFin = (df.loc[(df['br_stats'] == True),'teamPlacement']).mean()
                # avFin = round(avFin,1)
                # avg_fin_ls.append(avFin)

                # #Get Max Kills by Season
                # mxk = (df.loc[(df['br_stats'] == True),'kills']).max()
                # mx_kills_ls.append(mxk)

                # #kills/gm
                # kills_gm  = round(kills / games,2)
                # kills_list.append(kills_gm)

                # #deaths/gm
                # deaths_gm  = round(deaths / games,2)
                # deaths_list.append(deaths_gm)

                # #assists
                # assists = (df.loc[(df['br_stats'] == True),'assists']).sum()
                # ass_ls.append(assists)

                # #downs
                # downs = (df.loc[(df['br_stats'] == True),'downs']).sum()
                # downs = int(downs)
                # downs_list.append(downs)

                # #exec
                # execs = (df.loc[(df['br_stats'] == True),'executions']).sum()
                # exec_ls.append(execs)

                # #headshot
                # headshots = (df.loc[(df['br_stats'] == True),'headshots']).sum()
                # headshot = int(headshots)
                # head_ls.append(headshots)

                # #headshot %
                # h_pct = round(headshots / kills * 100, 1)
                # headpct_ls.append(h_pct)

                # #gulag w
                # gw = (df.loc[(df['br_stats'] == True),'gulagKills']).sum()
                # gw = int(gw)
                # gulag_w_ls.append(gw)


                # #gulag L
                # gl = (df.loc[(df['br_stats'] == True),'gulagDeaths']).sum()
                # gl= int(gl)
                # gulag_l_ls.append(gl)

                # #gulag pct
                # try:
                #     gp = round(gw / (gw+gl) * 100, 1)
                # except:
                #     gp = 0.0
                # gulag_pct_ls.append(gp)

def gulag_chart(pewpers):

    for p in pewpers:
        file_name = "user_files/"+ p+".csv"
        df = pd.read_csv (file_name)

        # avg_fin_ls = []
        # mx_kills_ls = []
        # kills_list = []
        # deaths_list = []
        # ass_ls =[]
        # downs_list = []
        # exec_ls =[]
        # head_ls= []
        # headpct_ls= []
        # gulag_w_ls = []
        # gulag_l_ls =[]
        # gulag_pct_ls =[]

        # games_list = []
        # wins_list = []
        # win_pct= []
        # kills_list = []

        # kd_list = []
        
        # top5_list =[]
        # top10_list = []
        # top25_list = []
        # top5_pct = []
        # top10_pct = []
        # top25_pct = []

        match_ls= []
        kd_ls =[]
        kd_rolling =[]
        seasons = ['all', 'mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2']

        for s in seasons:

            if s == 'all':
                #Get Games count
                games = (df.loc[((df['br_stats'] == True) & ((df['gulagKills'] == 1) | (df['gulagDeaths'] >=1))),['matchID','gulagKills','gulagDeaths']])
            else:
                games = (df.loc[((df['season'] == s) & ((df['gulagKills'] == 1) | (df['gulagDeaths']==1))),['matchID','gulagKills','gulagDeaths']])
            # print(games)
            if len(games) > 1:
                
                games.reset_index(inplace=True)
                # games['kd'] = games.kills / games.deaths

                games['gulagDeaths'].mask(games['gulagDeaths'] >= 1, 1, inplace=True)


                games['total_kills'] = games.gulagKills.cumsum()
                games['total_deaths'] = games.gulagDeaths.cumsum()
                games['gulag_pct'] = round((games.total_kills / (games.total_deaths + games.total_kills)),2)
                games['gulag_rolling'] = round((games.gulagKills.rolling(50).sum() / (games.gulagDeaths.rolling(50).sum() +games.gulagKills.rolling(50).sum())) ,2)
                games['gulag_rolling'].fillna(games['gulag_pct'], inplace=True)

                # games['kd_rolling'] = round(games['total_kd'].rolling(50).mean(),2)
                #print(games)

                games.drop(['matchID', 'gulagKills', 'gulagDeaths', 'total_kills', 'total_deaths'], axis=1, inplace=True)
                
                #reset index to begin with 1
                games['index'] = games['index'] - int(games.iloc[0]['index']-1)

                games.rename(columns={'index':'match'}, inplace=True)

            else:
                print('no matches for', p, s)

            # print(games)
            games = games.iloc[10:]
            print(games)
            out_dir ='./MWBattleData/chartGulag/{}'.format(p)
            try:
                os.mkdir(out_dir)
            except:
                print(out_dir, 'previously created')
            file_name = str(out_dir+'/'+s+'.csv')
            print('Create file: ' + file_name)
            games.to_csv(file_name, index=False)
            
            



            #     kills = (df.loc[(df['br_stats'] == True),['kills','deaths']])
            #     for k in kills:
            #         kd_ls.append(k)

            # print(match_ls)
            # print(kd_ls)
                # # deaths = (df.loc[(df['br_stats'] == True),'deaths'])
                # #Kills by Season
                


                # #Deaths by Season
                # deaths = (df.loc[(df['br_stats'] == True),'deaths']).sum()

                # #Get average finish
                # avFin = (df.loc[(df['br_stats'] == True),'teamPlacement']).mean()
                # avFin = round(avFin,1)
                # avg_fin_ls.append(avFin)

                # #Get Max Kills by Season
                # mxk = (df.loc[(df['br_stats'] == True),'kills']).max()
                # mx_kills_ls.append(mxk)

                # #kills/gm
                # kills_gm  = round(kills / games,2)
                # kills_list.append(kills_gm)

                # #deaths/gm
                # deaths_gm  = round(deaths / games,2)
                # deaths_list.append(deaths_gm)

                # #assists
                # assists = (df.loc[(df['br_stats'] == True),'assists']).sum()
                # ass_ls.append(assists)

                # #downs
                # downs = (df.loc[(df['br_stats'] == True),'downs']).sum()
                # downs = int(downs)
                # downs_list.append(downs)

                # #exec
                # execs = (df.loc[(df['br_stats'] == True),'executions']).sum()
                # exec_ls.append(execs)

                # #headshot
                # headshots = (df.loc[(df['br_stats'] == True),'headshots']).sum()
                # headshot = int(headshots)
                # head_ls.append(headshots)

                # #headshot %
                # h_pct = round(headshots / kills * 100, 1)
                # headpct_ls.append(h_pct)

                # #gulag w
                # gw = (df.loc[(df['br_stats'] == True),'gulagKills']).sum()
                # gw = int(gw)
                # gulag_w_ls.append(gw)


                # #gulag L
                # gl = (df.loc[(df['br_stats'] == True),'gulagDeaths']).sum()
                # gl= int(gl)
                # gulag_l_ls.append(gl)

                # #gulag pct
                # try:
                #     gp = round(gw / (gw+gl) * 100, 1)
                # except:
                #     gp = 0.0
                # gulag_pct_ls.append(gp)

def main():
        pewpers = ['DirtyUndies', 'cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator', 'TD994', 'MkeBeers54']

        #seasons that need to be udpated + all
        a_seasons = ['cw_2', 'all']

        #for reference / if we change format of tables
        # list_of_seasons = ['mw_1', 'mw_2', 'mw_3', 'mw_4', 'mw_5', 'mw_6', 'cw_1', 'cw_2', 'all']


        create_full_agg(pewpers) #all_match_data.csv
        create_user_files(pewpers) #user_files/x.csv
        season_totals(pewpers, a_seasons) # MWBattleData/'+s+'.csv'
        season_stats(pewpers, a_seasons) #MWBattleData/player_stats_X.csv'
        user_season_totals(pewpers) #MWBattleData/user_seaons_totals/
        user_mode_totals(pewpers) #MWBattleData/user_mode_totals/
        user_team_totals(pewpers) #MWBattleData/user_team_totals/
        daily_totals(pewpers)
        kd_chart(pewpers)
        gulag_chart(pewpers)
        daily_games(pewpers)
        weekly_kd_chart(pewpers)
        #testing


        #UPLOADS NEEDED
            # MWBattleData/
                # season_totals/ ---> season dashboard
                # season_stats/ ----> season stats
                # user_season_totals/ -->
                # user_mode_totals/ -->
                # user_team_totals/ -->
                # all_battle_data.json ---> main dashboard
                # weekly_battle_data.json  ---> weekly dashboard

            # once finished
                #chartKd/ folder
main()