#!/bin/bash

j="60"

while [ $j -lt 138 ]
do
    k=$[$j - 5]
    echo $k
	mv tmp-$j.gif tmp-$k.gif
	j=$[$j + 1]
done
