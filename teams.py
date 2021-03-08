import pandas as pd
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
        "objectiveMedalScoreSsKillJuggernaut", "objectiveMedalScoreSsKillManualTurret", 'objectiveBrLootChopperBoxOpen']

    plunder = "br_dmz"
    # pewpers = ['DirtyUndies', 'cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator']

    directory = r'./all_matches'
    bad_files = []

    #CSV to create
    with open('all_match_data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        # List of Full Match Files
        for filename in os.listdir(directory):
            fullPath = os.path.join(directory, filename)

            if filename.endswith(".json") :
                with open(fullPath) as f:
                    match = json.load(f)

            players = match['allPlayers']

            for p in players:
                try:
                    mode = str(p['mode'])
                    if "br_dmz" not in mode:
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
                    
                    # try:
                    #     print(p['player']['username'])
                    #     print(p['player'])
                    # except:
                    #     print(p['player'])
                    #print(p['player']['username'])
                    if filename not in bad_files:
                        bad_files.append(filename)
    print(bad_files)



def create_user_files(pewpers):

    # pewpers = ['cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator']

    directory = r'./all_matches'

    #Import CSV into Pandas DF
    df = pd.read_csv (r'all_match_data.csv')
    #print (df)

    #Create data_frames list
    dfs = []
    #Create User_DF
    for p in pewpers:
        # print(p)
        user_df = df[df['user'].str.match(p)]
        # print(user_df)
        # compile the list of dataframes you want to merge
        dfs.append(user_df)

    for d in dfs:
        g2 = df.groupby(['matchID']).agg(lambda col: ','.join(col))
        # print(g2)
        g2 = g2.sort_values(by=['matchID'])
        g2 = g2.reset_index()
        # print('---g2---')
        # print(g2)
        d = d.sort_values(by=['matchID'])
        d = d.reset_index()
        # print('--(d)df---')
        # print(d)
        # print(g2['user'])
        d['teammate1'] = g2['user']
        d[['teammate1','teammate2','teammate3', 'teammate4']] = d.teammate1.str.split(',',expand=True) 
        # # g['teammates']= new_column.reset_index(level=0, drop=True)
        # print(d['user'][0])
        file_name = str('user_files/'+d['user'][0]+ '.csv')
        print('Create file: ' + file_name)
        d.to_csv(file_name, index=True)



def main():
        pewpers = ['DirtyUndies', 'cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator', 'TD994', 'MkeBeers54']

        # Order
        # 1. run index.js to get all matches, followed by all_match_data csv file
        # 2. create
        create_full_agg(pewpers)
        create_user_files(pewpers)

main()