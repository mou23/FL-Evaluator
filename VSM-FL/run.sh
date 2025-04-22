#!/bin/bash

projects=("aspectj" "birt" "eclipse" "jdt" "swt" "tomcat")
type=$1  # baseline, clean

for proj in "${projects[@]}"; do
  command="python evaluator.py ../../FL-VSM/results-${type}/${proj} > ${type}_${proj}.txt"
  echo "Running ${proj} ${type}: $command"
  eval "$command"
done