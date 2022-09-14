#!/bin/bash
dir=$1
if [[ $# -eq 0 ]]; then
    echo "No directory name specified, exiting..."
    exit 1
fi
filename="students.txt"
lines=$(cat $filename)
echo "Creating submissions folder..."
for line in $lines
do
    echo "+ $line"
    mkdir -p $1/submissions/$line
done
echo "Copying template scripts..."
cp ../templates/*.sh $1/