#!/usr/bin/python

import sys
import time


class flightYear:
	"""
	Class for holding data for each year, with functions for 
	counting up totaldistances and time as each line of the 
	log document is read.
	"""

	def __init__(self, year_in):
		"""
		initialisation function for the class that sets the 
		year to the inputed year, distances and times to 0
		and the year to the inputed year.

		self: 		the class instance being initialised
		"""
		self.olc_distance = 0.0
		self.flown_distance = 0.0
		self.time_hours = 0
		self.time_minutes = 0
		self.year = year_in

	def addTime(self, line):
		"""
		adds the time difference between starting and landing 
		times to the class' time variables. Hours and minutes 
		are stored seperately to make the handeling easier

		self:		the class instance that the method is run on
		line: 		line of data from the txt file being read
		"""
		#extracting start and end times
		start_hr = int(line[2][:2])
		start_min = int(line[2][3:])
		end_hr = int(line[4][:2])
		end_min = int(line[4][3:])

		#calcuating total time
		total_hours = end_hr-start_hr

		#handeling minute change
		if start_min > end_min:
			total_hours -= 1
			total_mins = 60 - (start_min - end_min)
		else:
			total_mins = end_min - start_min

		#adding calculated hours and minutes
		self.time_hours += total_hours
		self.time_minutes += total_mins

		#handeling case for when minute counter goes over 60
		if self.time_minutes >= 60:
			self.time_hours += 1
			self.time_minutes %= 60

	def addFlownDist(self, line):
		"""
		extracts flown distance data from the line read by the file
		and adds it to the class instance.

		self: 		the class instance that the method is run on
		line:		the line of data being interpreted
		"""
		dist = line[6][:-2]
		if dist[0] != '-':
			self.flown_distance += float(dist)

	def addOLCDist(self, line):
		"""
		extracts olc distance data from the line read by the file
		and adds it to the class instance.

		self: 		the class instance that the method is run on
		line:		the line of data being interpreted
		"""
		dist = line[7][:-2]
		if dist[0] != '-':
			self.olc_distance += float(dist)

	def returnData(self):
		"""
		returns a formated string containing all of the data contained
		within the class instance.

		self: 		the class instance that the method is run on
		"""
		out_str = self.year +\
				"\tTime Flown:  " +\
				str(self.time_hours) + ":" + str(self.time_minutes) +\
				"\tDistance Flown:  " +\
				str(self.flown_distance) +\
				"\tOLC Distance Flown:  " +\
				str(self.olc_distance)

		return out_str

	def addLineInfo(self, line):
		"""
		brings together all of the informtion extraction functions into 
		a single function call 

		self: 		the class instance that the method is run on
		line: 		the line of data being read from the file
		"""
		self.addTime(line)
		self.addFlownDist(line)
		self.addOLCDist(line)

def main():
	"""
	main function that opens the file, reads the data, collects it in a dictionary of
	instances of the flightYear class and then prints out the formatted data
	"""
	#list to hold class instances for each year
	year_dict = {}

	#checking command line arguments
	if len(sys.argv) == 2:
		file_name = sys.argv[1]
	else:
		sys.exit("ERROR: Please specify a log file to be read.")

	#opening the file
	text = open(file_name, "r")
	lines = text.readlines()
	if len(lines) == 1:
		sys.exit("ERROR: log file is empty")

	#spliting each line on tabs
	for i in range(1, len(lines)):
		lines[i] = lines[i].split()
		current_line =  lines[i]

		#extract year
		date = current_line[1]
		year = "20" + date[6:]

		#adds new instance to the dict if it doesnt already exist
		if year not in year_dict:
			year_dict[year] = flightYear(year)

		#add info in line to the class instance of the correct year
		year_dict[year].addLineInfo(current_line)

	#getting a list of all keys in the dict, sorted by year
	keys = year_dict.keys()
	keys = sorted(keys, key = int)

	#printing data year by year
	total_olc_dist = 0
	total_norm_dist = 0
	total_time_hours = 0
	total_time_minutes = 0

	print "\n\nOutput data from" + file_name + "\n"

	for i in keys:
		#adding to final totals to print at the end
		total_olc_dist += year_dict[i].olc_distance
		total_norm_dist += year_dict[i].flown_distance
		total_time_hours += year_dict[i].time_hours
		total_time_minutes += year_dict[i].time_minutes
		if total_time_minutes >= 60:
			total_time_hours += 1
			total_time_minutes %= 60

		#printing the data for the year
		print year_dict[i].returnData()

	print "\nTotal OLC Distance Flown:\t", total_olc_dist
	print "Total Distance Flown:\t\t", total_norm_dist
	print "Total Time: \t\t\t" + str(total_time_hours) + ":" + str(total_time_minutes)

main()







