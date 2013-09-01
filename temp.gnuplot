set terminal pngcairo font "arial,10" size 640,480
		set output './symbols/2007.png'
		set xdata time

		set timefmt "%Y-%m-%d"
		set xrange ["2011-10-03":"2013-08-26"]
		set yrange [*:*]
		set datafile separator ","
		set multiplot

		set rmar 1
		set lmar 10
		set boxwidth 0.6 relative

		set size 1,0.7
		set origin 0,0.3

		plot './symbols/2007.week' using 1:2:4:3:5 with candlesticks  lt 1 

		set bmargin
		set format x
		set size 1.0,0.3
		set origin 0.0,0.0
		set tmargin 0
		set style fill solid
		set boxwidth 0.5 relative

		plot './symbols/2007.week' using 1:6 with  boxes lt 3
		unset multiplot 
		