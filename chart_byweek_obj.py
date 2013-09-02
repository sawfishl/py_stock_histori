#!/bin/python
import datetime
#datetime.date(2010,6,16).isocalendar()[1]


class symbol_obj:
	def __init__(self,path,major_path,symbol):
		import datetime
		import obj_major
		self.path = path
		self.major_path=major_path
		self.symbol = symbol	
		self.major = obj_major.major_obj(self.major_path)
	def make_url(self,ticker_symbol):
		base_url = "http://ichart.finance.yahoo.com/table.csv?s="
		return base_url + ticker_symbol
	def make_filename(self,ticker_symbol):
		return self.path  + self.symbol + ".csv"
	def update_symbol(self):
		import urllib
		import timeit
		try:
			start = timeit.default_timer()
			print 'Retrieving %s historical data' % self.symbol
			urllib.urlretrieve(self.make_url(self.symbol), self.make_filename(self.symbol))
			stop = timeit.default_timer()
			print 'Retrieving time %f s' % (stop-start)
		except urllib.ContentTooShortError as e:
			outfile = open(make_filename(self.symbol), "w")
			outfile.write(e.content)
			outfile.close()
	def weekofyear(self,csv_line):
		import string
		import datetime
		#extract date out
		date = [string.atoi(i) for i in csv_line.split(',')[0].split('-')]
		return datetime.date(date[0],date[1],date[2]).isocalendar()[1]
	def datestr2datetime(self,date_str):   #translate '2013-7-3' to datetime(2013,7,3)
		import datetime
		import string
		date_tuple = tuple([string.atoi(i) for i in date_str.split('-')])
		return datetime.date(*date_tuple)	
	def struct_week(self,weeks,filename='3481.TW.csv'):
		file = open(filename,'r')
		lines=file.readlines()
		file.close()
		current_week = self.weekofyear(lines[1])
		index = 1
		buffer = []
		struct = []
		for week in range(weeks):
			while(1):
				if(self.weekofyear(lines[index]) != self.weekofyear(lines[index+1])):
					buffer.append(lines[index])
					index = index +1
					break
				else:
					buffer.append(lines[index])
					#print lines[index]
					index = index+1
			struct.append(buffer)
			buffer = []
		return struct
	def week_summary(self,struct_week):
		import string
		date = struct_week[-1].split(',')[0]
		close = string.atof(struct_week[0].split(',')[4])
		popen = string.atof(struct_week[-1].split(',')[1])
		high = [string.atof(i.split(',')[2]) for i in struct_week]
		high.sort()
		highest = high[-1]
		low = [string.atof(i.split(',')[3]) for i in struct_week]
		low.sort()
		lowest = low[0]
		vol = [string.atof(i.split(',')[5]) for i in struct_week]
		volume = sum(vol)
		return (date,popen,highest,lowest,close,volume)
	def trans_day2week(self,folder,filename):
		import obj_major
		struct = self.struct_week(100,folder+filename)
		weekfile = open(folder+filename.split('.')[0]+'.week','wn')
		for line in struct:
			#query major_obj
			date = line[-1].split(',')[0]
			major_file_name = self.major.search_date(self.datestr2datetime(date)) #search_date return major file name refer to that date	
			major_current = obj_major.major_file_op(self.major_path,major_file_name) #class that operate with one major file
			week_major = major_current.symbol_query(self.symbol.split('.')[0]) #return major data of symbol at that week  !!!symbole in class is '3481.tw' but query('3481')
			#write ***.week file 
			#weekfile.write('%s,%f,%f,%f,%f,%f\n' % self.week_summary(line))
			if week_major:
				calc_net = week_major[2:4]+[week_major[2]-week_major[3]]+week_major[4:6]+[week_major[4]-week_major[5]]+week_major[6:8]+[week_major[6]-week_major[7]]
				temp =  self.week_summary(line) + tuple(calc_net)
			else:
				temp = self.week_summary(line) + (0,0,0,0,0,0,0,0,0) #except handle
			weekfile.write('%s,%f,%f,%f,%f,%f,%d,%d,%d,%d,%d,%d,%d,%d,%d\n' % temp)
		weekfile.close()
		#return start end date 
		return (self.week_summary(struct[0])[0], self.week_summary(struct[-1])[0])
	def gnuplot_script_gen(self,folder,filename,output,start_date,end_date):
		template = """set terminal pngcairo font "arial,10" size 640,480
		set output '%s%s'
		set xdata time

		set timefmt "%%Y-%%m-%%d"
		set xrange ["%s":"%s"]
		set yrange [*:*]
		set datafile separator ","
		set multiplot

		set rmar 1
		set lmar 10
		set boxwidth 0.6 relative

		set size 1,0.7
		set origin 0,0.3

		plot '%s%s' using 1:2:4:3:5 with candlesticks  lt 1 

		set bmargin
		set format x
		set size 1.0,0.3
		set origin 0.0,0.0
		set tmargin 0
		set style fill solid
		set boxwidth 0.5 relative

		plot '%s%s' using 1:6 with  boxes lt 3
		unset multiplot 
		"""
		script = template % (folder,output,start_date,end_date,folder,filename,folder,filename)
		script_file = 'temp.gnuplot'
		file = open(script_file,'wn')
		file.write(script)
		file.close
		return script_file
	def cvs_to_png(self):
		filename = self.symbol+'.csv'
		date =  self.trans_day2week(self.path,filename)
		script_file = self.gnuplot_script_gen(self.path,filename.split('.')[0]+'.week',filename.split('.')[0]+'.png',date[1],date[0])
		import os
		os.system('gnuplot %s' % script_file)
		return 0

class week_file_op:
	def __init__(self,path,week_file):
		self.path = path
		self.week_file=week_file
		week = open(path+week_file,'r')	
		lines = week.readlines()
		week.close()
		self.week_table = []
		for one_line in lines:
			temp = one_line.split(',')
			parsed = [temp[0]]+[float(i) for i in temp[1:6]]+[int(j) for j in temp[6:]]
			self.week_table.append(parsed)
		self.week_table.reverse()
		self.week_table = zip(*self.week_table)
		self.index = {
			'date':0,
			'open':1,
			'high':2,
			'low':3,
			'close':4,
			'vol':5,
			'f_overbuy':6,
			'f_oversell':7,
			'f_total':8,
			'i_overbuy':9,
			'i_oversell':10,
			'i_total':11,
			's_overbuy':12,
			's_oversell':13,
			's_total':14
		}
	def accmulation(self,item):
		target = self.week_table[self.index[item]]	
		accmu_list = []
		sum = 0
		for num in target:
			sum = num + sum
			accmu_list.append(sum)
			
		return accmu_list
	def mean_price(self,price,item):
		total = 0
		avg = 0
		avg_list = []
		price_list = self.week_table[self.index[price]]
		item_list = self.week_table[self.index[item]]
		for i in range(len(item_list)):
			print avg,price_list[i],item_list[i]
			if item_list[i] > 0:
				avg = (avg * total + price_list[i] * item_list[i]) / (total+item_list[i])
				avg_list.append(avg)
				total = total + item_list[i]
			else:
				avg_list.append(avg)
		return avg_list


if  __name__=='__mainn__':
	import obj_major
	import timeit
	csv_path = './symbols/'
	major_path ='./major/'
	obj = obj_major.major_obj(major_path)
	obj.update_major_file()
	#sym_cluster = ('006203','0057','2330','2498','0050','3481','2344','2883')
	#sym_cluster = ('2330','2498')
	sym_cluster = tuple(obj.symbols[0:200])
	obj_cluster = [symbol_obj(csv_path,major_path,sym+'.tw') for sym in sym_cluster]
	start = timeit.default_timer()	
	for obj in obj_cluster:
		obj.update_symbol()
		obj.cvs_to_png()
	stop = timeit.default_timer()	
	print 'Total processing time %fs' % (stop-start)
if __name__=='__main__':
	a = week_file_op('./symbols/','0050.week')
	print a.mean_price('close','f_total')

