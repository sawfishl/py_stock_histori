#!/bin/python

class major_obj:
	def __init__(self,path):
		self.path = path
		self.hash_major()
	def str_2_date(self,str_date):
		import datetime
		import string
		year = str_date[0:4]
		year = string.atoi(year)
		month = str_date[4:6]
		month = string.atoi(month)
		day = str_date[6:8]
		day = string.atoi(day)
		return datetime.date(year,month,day)
	def hash_major(self):
		import os
		self.file_list = [] 
		for csv_file in os.listdir(self.path):
			if csv_file.split('.')[1] == 'csv':
				#print csv_file +':\n'
				start_date = self.str_2_date(csv_file[0:8])
				end_date = self.str_2_date(csv_file[9:17])
				self.file_list.append((start_date,end_date,csv_file))
	def search_date(self,date):
		for csv_file in self.file_list:
			if date >= csv_file[0] and date <= csv_file[1]:
				return csv_file[2]
		return False
	def latest_date(self):
		date_array = [i[0] for i in self.file_list]
		date_array.sort()
		return date_array[-1]
		
				
	def list_dir(self):
		import os
		print os.listdir(self.path)

if __name__='__main__':
	test = major_obj('./major/')
	test.hash_major()
	import datetime
	print test.search_date(datetime.date(2013,7,3))
