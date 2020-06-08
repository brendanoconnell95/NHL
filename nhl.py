#Idea is a simple ELO model with a form component
#Implemented a decrease in K from a high initial value to account for sample size increasing over time

import csv
import math
from datetime import datetime

schedule = {}
team_list = ["Anaheim Ducks",
"Arizona Coyotes",
"Boston Bruins",
"Buffalo Sabres",
"Calgary Flames",
"Carolina Hurricanes",
"Chicago Blackhawks",
"Colorado Avalanche",
"Columbus Blue Jackets",
"Dallas Stars",
"Detroit Red Wings",
"Edmonton Oilers",
"Florida Panthers",
"Los Angeles Kings",
"Minnesota Wild",
"Montreal Canadiens",
"Nashville Predators",
"New Jersey Devils",
"New York Islanders",
"New York Rangers",
"Ottawa Senators",
"Philadelphia Flyers",
"Pittsburgh Penguins",
"San Jose Sharks",
"St. Louis Blues",
"Tampa Bay Lightning",
"Toronto Maple Leafs",
"Vancouver Canucks",
"Vegas Golden Knights",
"Washington Capitals",
"Winnipeg Jets"
]
ELO_list = {}
for team in team_list: 
	ELO_list.update({team:1500})

#start_date = '2017-10-04'
#end_date = '2017-11-04'
k_factor = 30
days_past = -1

def updateELO(match): 
		home = match.home
		away = match.away
		
		home_elo = ELO_list[home]
		away_elo = ELO_list[away]
		
		#calculate expected scores based on current ratings. Values between 0 and 1
		home_expected = 1/(1+math.pow(10,(away_elo-home_elo)/400))
		away_expected = 1/(1+math.pow(10,(home_elo-away_elo)/400))
		
		if match.HG > match.VG: 
			#home team won
			new_home = round(home_elo+k_factor*(1-home_expected),2)
			new_away = round(away_elo+k_factor*(0-away_expected),2)
		else: 
			#away team won NOT ACCOUNTING FOR OT OR SHOOTOUTS
			new_home = round(home_elo+k_factor*(0-home_expected),2)
			new_away = round(away_elo+k_factor*(1-away_expected),2)


		ELO_list.update({home:new_home})
		ELO_list.update({away:new_away})
		

	

	
class Match:
	def __init__(self, date, home, hg, away, vg):
		self.date = date
		self.home = home
		self.HG = hg
		self.away = away
		self.VG = vg
	
	def printMatch(self): 
		print(self.date, self.home, self.HG, self.away, self.VG)
		print()

with open("NHL_scores_1819.csv", newline='') as datafile: 
	puckreader = csv.DictReader(datafile, fieldnames=['Date','Visitor','VG','Home','HG'])
	
	#first pass to create team list
	for row in puckreader:
	
		cur_date = datetime.strptime(row['Date'],"%Y-%m-%d").date()
		if cur_date not in schedule: 
			schedule.update({cur_date: []})
			days_past+=1

			if days_past % 5 == 0: 
				k_factor -= (30-10)/36 		#Starting K minus final K divided by number of intervals

			#print(cur_date,":")
			#for team in ELO_list: 
				#print(team, ELO_list[team])
			
		cur_match = Match(cur_date, row['Home'], row['HG'], row['Visitor'], row['VG'])

		updateELO(cur_match)

		schedule[cur_date].append(cur_match)
	
	
for elem in sorted(ELO_list.items(), key = lambda x: x[1], reverse=True): 
	print(elem)
print("final K", round(k_factor,3))