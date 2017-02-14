#!/bin/bash
count=0
while [ $count -lt 10 ]
do
    (( count++ ))
    python autoDetect.py -i "$count.jpg"

    echo "$count.jpg"
done
