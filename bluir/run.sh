projects=("aspectj" "birt" "eclipse" "jdt" "swt" "tomcat")
type=$1  # baseline, clean

for proj in "${projects[@]}"; do
  command="python evaluator.py ../../FL-Bluir/results-${type}/BLUiR_${proj}/recommended ../../FL-Bluir/dataset/${proj}-updated-data.xml > ${type}_${proj}.txt"
  echo "Running ${proj} ${type}: $command"
  eval "$command"
done