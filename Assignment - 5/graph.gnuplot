# Set terminal and output file
set term png size 1024,786
set output 'graph.png'

# Define line styles
set style line 1 lc rgb "#1a9850" lw 1.5
set style line 2 lc rgb "black" lw 1.5
set style line 3 lc rgb "brown" lw 1.5
set style line 4 lc rgb "green" lw 1.5
set style line 5 lc rgb "orange" lw 1.5
set style line 6 lc rgb "#d73027" lw 1.5

# Start multiplot layout
set multiplot layout 3,1 title filename font ",14"
set yrange [0:]

# Plot Edge-Cut
set ylabel "Edge Cut"
set xlabel "Rounds"
set grid
plot filename using 1:2 with linespoints ls 1 title "Edge-Cut"

# Plot Swaps
set ylabel "Swaps"
set xlabel "Rounds"
set grid
plot filename using 1:3 with linespoints ls 2 title "Swaps"

# Plot Migrations
set ylabel "Migrations"
set xlabel "Rounds"
set grid
plot filename using 1:4 with linespoints ls 3 title "Migrations"

# End multiplot
unset multiplot
