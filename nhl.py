import csv

with open("NHLdata.csv", newline='') as datafile: 
	puckreader = csv.reader(datafile, delimiter=',')
	for row in puckreader: 
		print(', '.join(row))