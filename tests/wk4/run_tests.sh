#!/bin/bash
parent=$(pwd)

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
        [ -e test_results.txt ] && rm test_results.txt
        echo "Testing Functions..." >> test_results.txt
        echo "1" | pytest -s -vv test_skbin_functions.py >> test_results.txt
        echo "Demoing Program..." >> test_results.txt
        pytest --capture=sys -v test_skbin_demo.py >> test_results.txt
        rm test_*.py
        cd $parent
    fi
done