#!/bin/bash i=1 max=$CURRENT_NUM while [[ $i -le $max ]]; do wget "http://www.snailinaturtleneck.com/comics/images/siat$(printf "%04d" $i).jpg" -O siat$(printf "%04d" $\ i).jpg let "i=$i+1" done 
