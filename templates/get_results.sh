#!/bin/bash
resultsfile=test_results.txt

for dir in submissions/*; do
    ufmtname=${dir#*/}
    name=${ufmtname//_/" "}
    echo ""
    if [ -z "$(ls -A $dir | grep $resultsfile)" ]; then
        echo "directory for $name has no result, skipping..."
    else
        echo "$name's Results"
        
        test_example=$(cat $dir/$resultsfile | grep "test_example PASS" | wc -l)
        
        echo "Example test... [ $test_example ]"
    fi
done