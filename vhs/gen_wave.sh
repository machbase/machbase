#!/bin/bash
angle=0
step_angle=24
sinval=0
cosval=0
PI=3.14159

while [ 1 ]
do
    ts=`date +"%s"`
    sinval=$(awk "BEGIN{ printf \"%.6f\", (sin($angle*($PI/180)))}")
    cosval=$(awk "BEGIN{ printf \"%.6f\", (cos($angle*($PI/180)))}")
    echo "wave.sin,$ts,$sinval"
    echo "wave.cos,$ts,$cosval"
    sleep 1
    angle=$((angle+step_angle))
done
