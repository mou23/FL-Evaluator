import sys
import csv
import json

def create_csv(data):
    results = {
        1: [],
        5: [],
        10: []
    }

    for top in [1, 5, 10]:
        count = 0
        total_bug = 0
        for key, value in data.items():
            # print(key)
            suspicious_files = value['results']
            # print(suspicious_files)
            fixed_files = value['truth']
            # print(fixed_files) 
            # print(suspicious_files[0:top])
            for fixed_file in fixed_files:
                if fixed_file in suspicious_files[0:top]:
                    results[top].append(key)
                    count = count + 1
                    break
            total_bug = total_bug + 1
        print('accuracy@', top, count, total_bug, (count*100/total_bug))

    with open('localized_bugs_'+project+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['Accuracy@1', 'Accuracy@5', 'Accuracy@10'])
        
        max_length = max(len(results[1]), len(results[5]), len(results[10]))
        
        for i in range(max_length):
            row = []
            for k in [1, 5, 10]:
                if i < len(results[k]):
                    row.append(results[k][i])
                else:
                    row.append('')
            writer.writerow(row)


project = sys.argv[1]     
with open(project+'/results.json', 'r') as file:
    data = json.load(file)

create_csv(data)