#!/bin/bash
resultsfile=test_results.txt

for dir in submissions/*; do
    ufmtname=${dir#*/}
    name=${ufmtname//_/" "}
    echo ""
    if [ -z "$(ls -A $dir | grep $resultsfile)" ]; then
        echo "directory for $name has no result, skipping..."
    else
        echo ""
        echo "$name's Results"
        test_written_fn=$(cat $dir/test_results.txt | grep "test_all_functions_are_written SUBPASS" | wc -l)
        test_get_price=$(cat $dir/test_results.txt | grep "test_get_price SUBPASS" | wc -l)
        test_get_ingredients=$(cat $dir/test_results.txt | grep "test_get_ingredients SUBPASS" | wc -l)
        test_check_stock_ok=$(cat $dir/test_results.txt | grep "test_check_stock_available SUBPASS" | wc -l)
        test_check_stock_ng=$(cat $dir/test_results.txt | grep "test_check_stock_unavailable PASSED" | wc -l)
        test_update_stock=$(cat $dir/test_results.txt | grep "test_update_stock SUBPASS" | wc -l)
        lint_score=$(tail -n 4 $dir/test_results.txt | grep "." | tail -n 1)
        echo "Functions written... [ $test_written_fn ]"
        echo "Get price... [ $test_get_price ]"
        echo "Get ingredients... [ $test_get_ingredients ]"
        echo "Check stock available... [ $test_check_stock_ok ]"
        echo "Check stock not available... [ $test_check_stock_ng ]"
        echo "Update stock... [ $test_update_stock ]"
        echo "Lint score... [ $lint_score ]"
    fi
done
