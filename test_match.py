import pandas as pd
import json
import csv
import os

def main():

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
        "objectiveMedalScoreSsKillJuggernaut"]

    plunder = "br_dmz"
    pewpers = ['DirtyUndies', 'cdawg009', 'horseboat8', 'mooseattack90', 'BEEFsnake22', 'The Defecator']

    directory = r'./full_matches'
    bad_files = []

    #CSV to create
    with open('xx_match_data.csv', 'w') as csvfile:
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


main()