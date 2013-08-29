import urllib

"""http://www.twse.com.tw/ch/trading/fund/TWT54U/TWT54U_print.php?begin_date=20130826&end_date=20130827&report_type=&language=ch&select2=ALLBUT0999&save=csv"""
url = 'http://www.twse.com.tw/ch/trading/fund/TWT54U/TWT54U_print.php?begin_date=%s&end_date=%s&report_type=&language=ch&select2=ALLBUT0999&save=csv'
#urllib.urlretrieve(url,'major.csv')


import datetime
today = datetime.date.today()
day_shift = datetime.timedelta(days=1)


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


folder = './major/'
for date_pair in date_tuple:
	print 'Downloading date between'+date_pair[0]+'-'+date_pair[1]
	urllib.urlretrieve(url % date_pair,folder+'%s-%s.csv' % (date_pair[0],date_pair[1]))
	print 'Download done!'
