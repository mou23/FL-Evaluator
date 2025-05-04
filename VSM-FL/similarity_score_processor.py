import sys
import json
import os
import csv

def process_similarity_scores():
    with open(f"similarity_score_{project_name}.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["bug_id", "avg_score", "similarity_score_of_first_correct_file"])

        for current_bug_data in bug_data:
            score = 0
            top_k = 10
            for k, v in list(current_bug_data['suspicious_file_data'].items())[:top_k]:
                score += v
            avg_score = score / top_k

            fixed_files = current_bug_data['fixed_files']
            similarity_score_of_first_correct_file = None
            for k, v in current_bug_data['suspicious_file_data'].items():
                if k in fixed_files:
                    similarity_score_of_first_correct_file = v
                    break

            writer.writerow([current_bug_data["id"], avg_score, similarity_score_of_first_correct_file])
           

def get_bug_data(directory_path):
    bugs = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            current_file = os.path.join(root, file)
            if not current_file.endswith('.json'):
                continue
            bug_data = {}
            with open(current_file, 'r') as f:
                data = json.load(f)
                if 'id' not in data or 'results' not in data or 'truth' not in data:
                    print(f"Invalid data in file: {current_file}")
                    continue
            bug_data['id'] = data['id']
            bug_data['suspicious_file_data'] = data['results']
            bug_data['fixed_files'] = data['truth']
            bugs.append(bug_data)

    return bugs

project_name = sys.argv[1] 
result_directory = sys.argv[2]

bug_data = get_bug_data(result_directory)
process_similarity_scores()
