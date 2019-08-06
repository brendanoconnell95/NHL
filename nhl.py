#Idea is a simple ELO model with a form component

import csv
import math
from datetime import datetime

schedule = {}
team_list = []
ELO_list = {}
start_date = '2017-10-04'
end_date = '2017-11-04'
k_factor = 10

with open("NHL_scores_1819.csv", newline='') as datafile: 
	puckreader = csv.DictReader(datafile, fieldnames=['Date','Visitor','VG','Home','HG'])
	
	for row in puckreader:
		if row['Home'] not in team_list: 
			team_list.append(row['Home'])
	
		cur_date = datetime.strptime(row['Date'],"%Y-%m-%d").date()
		if cur_date not in schedule: 
			schedule.update({cur_date: []})
			#schedule.sort()
		
		#if match is not in schedule, add it
		#Match will never be! May be useful to check in future though
		match = row['Home']+ ": " +row['HG']+ ", " +row['Visitor']+ ": " +row['VG']
		if match not in schedule[cur_date]:
			a_list = schedule[cur_date]
			a_list.append(match)
			schedule.update({cur_date : a_list})
		else: 
			print("skipped match")
for team in team_list: 
	ELO_list.update({team: 1500})
		
def updateELO(match): 
		sides = match.split(", ")
		home = sides[0].split(":")
		away = sides[1].split(":")
		
		home_elo = ELO_list.get(home[0])
		away_elo = ELO_list.get(away[0])
		
		#calculate expected scores based on current ratings. Values between 0 and 1
		home_expected = 1/(1+math.pow(10,(away_elo-home_elo)/400))
		away_expected = 1/(1+math.pow(10,(home_elo-away_elo)/400))
		
		if home[1] > away[1]: 
			#home team won
			new_home = home_elo+k_factor*(1-home_expected)
			new_away = away_elo+k_factor*(0-away_expected)
		else: 
			#away team won
			new_home = home_elo+k_factor*(0-home_expected)
			new_away = away_elo+k_factor*(1-away_expected)


		ELO_list.update({home[0]:new_home})
		ELO_list.update({away[0]:new_away})


for day in schedule: 
	#need to read the results of the day and update the ELO rankings
	matches = schedule[day]
	#print(day, matches)

	for match in matches: 
		#print(match)	
		updateELO(match)


# for elem in sorted(ELO_list.items(), key=lambda x: x[1], reverse=True): 
	# print(elem)

#-------------------------BACK TESTING---------------------------------
with open("NHL_odds_1819.csv", newline="", encoding='utf-8-sig') as oddsfile: 
	oddsreader = csv.reader(oddsfile)
	for row in oddsreader:
		#need to convert dates to create schedule

		if len(row[0]) == 4: 
			cur_month = row[0][0:2]
			cur_day = row[0][2:4]
			cur_year = "2018"
		else:
			cur_year = "2019"
			#need to append a '0' to the month
			cur_month = "0" + row[0][0]
			cur_day = row[0][1:3]
		
		cur_date = datetime.strptime(cur_month+cur_day+cur_year, "%m%d%Y").date()
		print(cur_date)

		#opening lines are 5th col, closing are 6th
		#print(row[4])
































