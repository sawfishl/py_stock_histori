#!/bin/python
import datetime
#datetime.date(2010,6,16).isocalendar()[1]

class symbol_obj:
	def __init__(self,path,symbol):
		self.path = path
		self.symbol = symbol	
	def make_url(self,ticker_symbol):
		base_url = "http://ichart.finance.yahoo.com/table.csv?s="
		return base_url + ticker_symbol
	def make_filename(self,ticker_symbol):
		return self.path  + self.symbol + ".csv"
	def update_symbol(self):
		import urllib
		try:
			urllib.urlretrieve(self.make_url(self.symbol), self.make_filename(self.symbol))
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
		struct = self.struct_week(100,folder+filename)
		weekfile = open(folder+filename.split('.')[0]+'.week','wn')
		for line in struct:
			#write ***.week file 
			weekfile.write('%s,%f,%f,%f,%f,%f\n' % self.week_summary(line))
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


		plot '%s%s' using 1:6 with  impulses lt 3
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

if  __name__=='__main__':
	folder = './new_test/'
	sym_cluster = ('2330','2498','0050','3481','2344','2883')
	obj_cluster = [symbol_obj(folder,sym+'.tw') for sym in sym_cluster]
	
	for obj in obj_cluster:
		obj.update_symbol()
		obj.cvs_to_png()

	
