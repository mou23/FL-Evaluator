projects=("aspectj" "birt" "eclipse" "jdt" "swt" "tomcat")
type=$1  # baseline, clean

for proj in "${projects[@]}"; do
  command="python evaluator.py ../../FL-BRTracer/results-${type}/BRTracer_${proj} ../../FL-BRTracer/dataset/${proj}-updated-data.xml > ${type}_${proj}.txt"
  echo "Running ${proj} ${type}: $command"
  eval "$command"
done