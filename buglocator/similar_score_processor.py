from bug_data_processor import get_bug_data_with_similarity_score
import sys
import csv

project_name =sys.argv[1]
result_directory = sys.argv[2] #'../../dataset/temp/BugLocator_test_run'
bug_report_file = sys.argv[3] #'../../dataset/aspectj-filtered.xml'
bug_data = get_bug_data_with_similarity_score(bug_report_file, result_directory)


def calculate_avg_similarity_scores():
    with open(f"similarity_score_{project_name}.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["bug_id", "avg_score", "similarity_score_of_first_correct_file"])

        for current_bug_data in bug_data:
            score = 0
            top_k = 10
            for k, v in list(current_bug_data['suspicious_file_data'].items())[:top_k]:
                score += v
            avg_score = score / top_k

            fixed_files = current_bug_data['files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            similarity_score_of_first_correct_file = None
            for k, v in current_bug_data['suspicious_file_data'].items():
                if k in fixed_files:
                    similarity_score_of_first_correct_file = v
                    break

            writer.writerow([current_bug_data["bug_id"], avg_score, similarity_score_of_first_correct_file])

calculate_avg_similarity_scores()