set terminal pngcairo font "arial,10" size 720,720
		output = './symbols/9958.png'
		file = './symbols/9958.week'
		set title '9958'
		set output output
		set xdata time

		set timefmt "%Y-%m-%d"
		set xrange ["2011-11-07":"2013-09-30"]
		set yrange [*:*]
		set datafile separator ","
		set multiplot

		set rmar 1
		set lmar 10
		set boxwidth 0.6 relative
		set grid ytics 
		set bmargin 0

		set size 1,0.4
		set origin 0,0.6
		unset xtics

		plot file using 1:2:4:3:5 with candlesticks  lt 1 
		set bmargin 0
		set format x
		set size 1,0.2
		set origin 0.0,0.4
		set tmargin 0
		set style fill solid
		set boxwidth 0.5 relative
		unset xtics
		unset title
		plot file using 1:6 with  boxes lt 3
		set bmargin 0
		set format x
		set size 1,0.2
		set origin 0.0,0.2
		set tmargin 0
		set boxwidth 0.5 relative
		unset title


		plot file using 1:16 with line lt rgb 'red',			file using 1:17 with line lt rgb 'blue',			file using 1:18 with line lt rgb 'green'
		set bmargin
		set format x
		set size 1,0.2
		set origin 0.0,0.0
		set tmargin 0
		set boxwidth 0.5 relative

		unset title
		set xtics
		plot file using 1:19 with line lt rgb 'red',			file using 1:20 with line lt rgb 'blue',			file using 1:21 with line lt rgb 'green'


		unset multiplot 

		

	
		