#Idea is a simple ELO model with a form component

import csv
import math

schedule = {}
team_list = []
ELO_list = {}
start_date = '2017-10-04'
end_date = '2017-11-04'
k_factor = 30

with open("NHL1819.csv", newline='') as datafile: 
	puckreader = csv.DictReader(datafile, fieldnames=['Date','Visitor','VG','Home','HG'])
	#first pass to create team list and schedule
	for row in puckreader:
		if row['Home'] not in team_list: 
			team_list.append(row['Home'])
	
		if row['Date'] not in schedule: 
			schedule.update({row['Date'] : []})
			#schedule.sort()
		
		if row['Home']+row['HG']+row['Visitor']+row['VG'] not in schedule[row['Date']]:
			new_list = schedule[row['Date']]
			new_list.append(row['Home']+ ": " +row['HG']+ ", " +row['Visitor']+ ": " +row['VG'])
			schedule.update({row['Date'] : new_list})
		
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
	#determine the result of the match
	

	for match in matches: 
		#print(match)	
		updateELO(match)


print(sorted(ELO_list.items(), key=lambda x: x[1], reverse=True))
