from bug_data_processor import get_bug_data_with_similarity_score
import sys
import csv

project_name =sys.argv[1]
result_file = sys.argv[2] #'tomcat_ranked_result_mapped.csv'
bug_report_file = sys.argv[3] #'../../dataset/tomcat-updated-data.xml'
type = sys.argv[4]
index = int(sys.argv[5])
bug_data = get_bug_data_with_similarity_score(bug_report_file, result_file, index)

def process_similarity_scores():
    with open(f"similarity_score_{project_name}_{type}.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["bug_id", "avg_score", "similarity_score_of_first_correct_file"])

        for current_bug_data in bug_data:
            score = 0
            top_k = 10
            try:
                for k, v in list(current_bug_data['suspicious_file_data'].items())[:top_k]:
                    score += v
                avg_score = score / top_k

                fixed_files = current_bug_data['fixed_files'].split('.java')
                fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
                similarity_score_of_first_correct_file = None
                for k, v in current_bug_data['suspicious_file_data'].items():
                    if k in fixed_files:
                        similarity_score_of_first_correct_file = v
                        break

                writer.writerow([current_bug_data["bug_id"], avg_score, similarity_score_of_first_correct_file])
            except Exception as Error:
                print(f"Error processing bug {current_bug_data['bug_id']}: {str(Error)}")
                continue

process_similarity_scores()