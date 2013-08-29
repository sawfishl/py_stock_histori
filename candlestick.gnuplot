set terminal pngcairo font "arial,10" size 640,480
set output './TW/2330.png'
set xdata time

set timefmt"%Y-%m-%d"
set xrange ["2012-1-1":"2013-8-26"]
set yrange [*:*]
set datafile separator ","
set multiplot

set rmar 1
set lmar 10
set boxwidth 0.6 relative

set size 1,0.7
set origin 0,0.3

plot './TW/2330.week' using 1:2:4:3:5 with candlesticks  lt 1 

set bmargin
set format x
set size 1.0,0.3
set origin 0.0,0.0
set tmargin 0


plot './TW/2330.week' using 1:6 with  impulses lt 3
unset multiplot
