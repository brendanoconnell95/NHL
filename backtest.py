#Testing file for NHL ELO model
import csv, math 
from datetime import datetime

schedule = {}


#-------------------------BACK TESTING---------------------------------
class oddsObj:
	def __init__(self, date, team, odds):
		self.team = team
		self.odds = odds
		self.date = date
		
	def printOdds(self):
		print(self.date, self.team, self.odds)
		print()

class Match:
	#takes 2 odds objects, for home and away
	def __init__(self, home_obj, away_obj):
		if home_obj.date != away_obj.date: 
			print("BAD MATCH")
			self.home = "home"
			self.away = "away"
			self.h_odds = "0"
			self.a_odds = "0"
			self.date = "0000-00-00"

		else: 
			self.home = home_obj.team
			self.away = away_obj.team
			self.h_odds = home_obj.odds
			self.a_odds = away_obj.odds
			self.date = home_obj.date

	def printMatch(self): 
		print(self.date, self.home, self.h_odds, self.away, self.a_odds)
	
	def clear(self):
		self.home = "home"
		self.away = "away"
		self.h_odds = 0
		self.a_odds = 0
		self.date = "0000-00-00"

#convert string of American odds to float of decimal odds
def convertAmericantoDecimal(odd):
	if odd[0] == "+": 
		decimal_odd = 1+int(odd[1:])/100
	elif odd[0] == "-": 
		if int(odd) == 0: 
			decimal_odd = 1.0
		else: 
			decimal_odd = 1+100/int(odd[1:]) 
	else: 
		print("BAD ODDS")
		decimal_odd = 0
	return round(decimal_odd,3)

with open("NHL_odds_1819.csv", newline="", encoding='utf-8-sig') as oddsfile: 
	oddsreader = csv.reader(oddsfile)
	
	homeBool = False
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
		if cur_date not in schedule:
			schedule.update({cur_date:[]})
		
		#team is 3rd col, opening line in 4, closing line in 5
		cur_odd = oddsObj(cur_date, row[3], row[4])

		if homeBool:
			#create a match from previous odd (away side) and this line's odd (home side) and add it to the schedule
			match = Match(prev_odd, cur_odd)
			schedule[cur_date].append(match)
			homeBool = not homeBool
		
		else: 
			homeBool = not homeBool

		prev_odd = cur_odd
		

				
for day in schedule: 
	for match in schedule[day]: 
		match.printMatch()
	

# for day in scores_schedule: 
# 	#need to check scores and odds lists for each day
# 	scores_schedule[day].sort(key=alphaSort)
# 	lines_schedule[day].sort(key=alphaSort)
# 	for day in scores_schedule: 
# 		results = scores_schedule[day]
# 		for elem in results:
# 			elem.printScore()
		# lines = lines_schedule[day]
		# for i in range(len(results)): 
			# if results[i].home == lines[i].home: 
				# print("It worked!")
			# else:
				# print("Not a match")
	
# for elem in sorted(ELO_list.items(), key=lambda x: x[1], reverse=True): 
	# print(elem)