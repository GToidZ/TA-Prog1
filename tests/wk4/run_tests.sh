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
        echo "1" | pytest -s -vv test_skbin_functions.py >> test_results.txt

        rm test_*.py

        echo "==========" >> $resultsfile
        echo "Linting..." >> $resultsfile
        pylint *.py --exit-zero --disable=R >> $resultsfile 2>&1

        cd $parent
    fi
done
