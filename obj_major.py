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
			if csv_file[-3:-1] == 'cs':
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
		#return latest monday
		date_array = [i[0] for i in self.file_list]
		date_array.sort()
		return date_array[-1]
	def oldest_date(self):
		date_array = [i[0] for i in self.file_list]
		date_array.sort()
		return date_array[0]
	def update_major_file(self):
		import urllib
		url = 'http://www.twse.com.tw/ch/trading/fund/TWT54U/TWT54U_print.php?begin_date=%s&end_date=%s&report_type=&language=ch&select2=ALLBUT0999&save=csv'
		import datetime
		today = datetime.date.today()
		day_shift = datetime.timedelta(days=1)
		#creating all mon fri date array
		date_array = []
		for i in range(1000):
			date = today-i*day_shift
			weekday = date.isocalendar()[2]
			if i == 0 and weekday <=5 and weekday >=1:
				date_array.append(date)
			elif weekday ==1 or  weekday == 5:
				date_array.append(date)
		date_tuple = []
		for i in range(140):
			fri = date_array[2*i] 
			mon = date_array[2*i+1]
			fri_str = '%04d%02d%02d' % (fri.year,fri.month,fri.day)
			mon_str= '%04d%02d%02d' % (mon.year,mon.month,mon.day)
			date_tuple.append((mon_str,fri_str))
			if mon ==self.latest_date():
				break
		print date_tuple
		#kill latest date (may not complete)
		import os
		os.remove(self.path + self.search_date(self.latest_date()) )

		for date_pair in date_tuple:
			print 'Downloading date between'+date_pair[0]+'-'+date_pair[1]
			urllib.urlretrieve(url % date_pair,self.path+'%s-%s.csv' % (date_pair[0],date_pair[1]))
			print 'Download done!'
			


				
	def list_dir(self):
		import os
		print os.listdir(self.path)

if __name__=='__main__':
	test = major_obj('./major/')
	test.hash_major()
	import datetime
	print test.search_date(datetime.date(2013,7,3))
