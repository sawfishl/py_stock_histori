#!/bin/python
import datetime
#datetime.date(2010,6,16).isocalendar()[1]

def weekofyear(csv_line):
	import string
	import datetime
	#extract date out
	date = [string.atoi(i) for i in csv_line.split(',')[0].split('-')]
	return datetime.date(date[0],date[1],date[2]).isocalendar()[1]

def struct_week(weeks,filename='3481.TW.csv'):
	file = open(filename,'r')
	lines=file.readlines()
	file.close()


	current_week = weekofyear(lines[1])
	index = 1
	buffer = []
	struct = []
	for week in range(weeks):
		while(1):
			if(weekofyear(lines[index]) != weekofyear(lines[index+1])):
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

def week_summary(struct_week):
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

def trans_day2week(folder,filename):
	struct = struct_week(100,folder+filename)
	weekfile = open(folder+filename.split('.')[0]+'.week','wn')
	for line in struct:
		weekfile.write('%s,%f,%f,%f,%f,%f\n' % week_summary(line))
	weekfile.close()
	#return start end date 
	return (week_summary(struct[0])[0], week_summary(struct[-1])[0])
 __name__=='__main__':
	folder = './'
	filename = '2330.tw.csv'
	
	print trans_day2week(folder,filename)
	
	
	
