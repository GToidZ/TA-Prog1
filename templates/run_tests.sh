#!/bin/bash
parent=$(pwd)
resultsfile=test_results.txt

# For each folder
for dir in submissions/*; do
    ufmtname=${dir#*/}
    name=${ufmtname//_/" "}
    if [ -z "$(ls -A $dir)" ]; then
        echo "directory for $name empty, skipping..."
    else
        echo "testing for $name..."
        cp test_*.py $dir
        cd $dir
        [ -e $resultsfile ] && rm $resultsfile
        
        echo "Testing..." >> $resultsfile
        python -m unittest -v test_example.py >> $resultsfile
        
        rm test_*.py
        cd $parent
    fi
done