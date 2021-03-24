#!/usr/local/bin/ bash

dir=/Users/cott/Repos/COD_Warzone_Fetch_Matches

python3=/usr/local/bin/python3.9
node=/usr/local/bin/node

echo "start:" $(date)

now=$(date  '+20%y-%m-%d')
yest=$(date -v -1d '+20%y-%m-%d')

season='cw_2'

# echo $now 
# echo $yest

cd $dir
# Get new matches
echo "Get New Matches, running NODE" | ts
AWS_PROFILE=personal node index_casey.js | ts

#Generate new files
echo "Generate New Files...running PYTHON" | ts
python3 teams.py | ts


#Upload files to S3
echo "Upload Files to S3" | ts



#UPLOAD everything
# aws s3 cp --profile personal  MWBattleData/  s3://houstontrashtros.com/wz/MWBattleData --recursive --exclude "*.DS_Store"


# #chartKd
# aws s3 cp --profile personal  MWBattleData/chartKd/  s3://houstontrashtros.com/wz/MWBattleData/chartKd --recursive --exclude "*.DS_Store"

################
##      IF SEASON FILES HAVE NEW COLUMNS YOU NEED TO PUSH NEW FILES TO S3
###############


# #daily_totals (today only and yest)
aws s3 cp --profile personal  MWBattleData/daily_totals/$now.csv  s3://houstontrashtros.com/wz/MWBattleData/daily_totals/$now.csv 
aws s3 cp --profile personal  MWBattleData/daily_totals/$yest.csv  s3://houstontrashtros.com/wz/MWBattleData/daily_totals/$yest.csv

aws s3 cp --profile personal  MWBattleData/daily_games/$now.csv  s3://houstontrashtros.com/wz/MWBattleData/daily_games/$now.csv

#season_stats
aws s3 cp --profile personal  MWBattleData/season_stats/all.csv  s3://houstontrashtros.com/wz/MWBattleData/season_stats/all.csv
aws s3 cp --profile personal  MWBattleData/season_stats/$season.csv  s3://houstontrashtros.com/wz/MWBattleData/season_stats/$season.csv


#season_totals
aws s3 cp --profile personal  MWBattleData/season_totals/all.csv  s3://houstontrashtros.com/wz/MWBattleData/season_totals/all.csv
aws s3 cp --profile personal  MWBattleData/season_totals/$season.csv  s3://houstontrashtros.com/wz/MWBattleData/season_totals/$season.csv

#user_mode_totals
aws s3 cp --profile personal  MWBattleData/user_mode_totals/  s3://houstontrashtros.com/wz/MWBattleData/user_mode_totals/ --recursive --exclude "*.DS_Store"

#user_season_totals
aws s3 cp --profile personal  MWBattleData/user_season_totals/  s3://houstontrashtros.com/wz/MWBattleData/user_season_totals/ --recursive --exclude "*.DS_Store"

#user_team_totals
aws s3 cp --profile personal  MWBattleData/user_team_totals/  s3://houstontrashtros.com/wz/MWBattleData/user_team_totals/ --recursive --exclude "*.DS_Store"

aws s3 cp --profile personal  MWBattleData/chartKd/  s3://houstontrashtros.com/wz/MWBattleData/chartKd/ --recursive --exclude "*.DS_Store"
aws s3 cp --profile personal  MWBattleData/chartGulag/  s3://houstontrashtros.com/wz/MWBattleData/chartGulag/ --recursive --exclude "*.DS_Store"
aws s3 cp --profile personal  MWBattleData/chartWeekKd/  s3://houstontrashtros.com/wz/MWBattleData/chartWeekKd/ --recursive --exclude "*.DS_Store"

#user_files/
#aws s3 cp --profile personal  user_files/  s3://houstontrashtros.com/wz/user_files/ --recursive --exclude "*.DS_Store"


date +"%m/%d/20%y, %r" > MWBattleData/date.txt
aws s3 cp --profile personal  MWBattleData/date.txt  s3://houstontrashtros.com/wz/MWBattleData/date.txt
