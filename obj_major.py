#!/bin/python

class major_obj:
	def __init__(self,path):
		self.path = path
		self.hash_major()
		self.symbol_list()
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
		date_array = [i[0] for i in self.file_list]
		date_array.sort()
		#return lateest monday
		return date_array[-1]
	def oldest_date(self):
		date_array = [i[0] for i in self.file_list]
		date_array.sort()
		return date_array[0]
	def symbol_list(self):
		sorted_list = sorted(self.file_list,key=lambda date:date[1])
		major_file = open(self.path+sorted_list[0][2],'r')
		#avoid first header line
		major_file.readline()
		major_file.readline()
		##
		major_lines = major_file.readlines()
		major_file.close()
		self.symbols = []
		for line in major_lines:	
			sym = line.split(',')[0].split(' ')[0]
			if len(sym) <=4:
				self.symbols.append(sym)
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
		#kill latest date (may not complete)
		import os
		os.remove(self.path + self.search_date(self.latest_date()) )
		import timeit
		for date_pair in date_tuple:
			print 'Retrieving major data '+date_pair[1]+'-'+date_pair[1]
			start = timeit.default_timer()
			urllib.urlretrieve(url % date_pair,self.path+'%s-%s.csv' % (date_pair[0],date_pair[1]))
			stop = timeit.default_timer()
			print 'Retrieving time %f s' % (stop-start)
		self.hash_major()
	def list_dir(self):
		import os
		print os.listdir(self.path)

class major_file_op:
	def __init__(self,path,filename):
		self.path = path
		self.filename = filename
		major_file = open(path+filename,'r')
		self.major_lines = major_file.readlines()
		major_file.close()
	def parse_num(self,num_str):
		import string
		#8,558,000 -> 8558000
		num_join = string.join(num_str.split(','),'')
		return string.atoi(num_join)
	def symbol_query(self,symbol):
		for line in self.major_lines:
			data_set = line.split(',')
			if len(data_set) >= 1 and data_set[0].find(symbol) >=0:
				vec = (1,3,5,7,9,11)
				return [data_set[0],data_set[1]]+[self.parse_num(line.split('"')[i]) for i in vec]
		return False	

if __name__=='__main__':
	test = major_obj('./major/')
	test.hash_major()
	import datetime
	print test.search_date(datetime.date(2013,7,3))
	july_3 = major_file_op('./major/',test.search_date(datetime.date(2013,7,3)))
	print july_3.symbol_query('0050')
