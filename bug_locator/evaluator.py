from bug_data_processor import get_bug_data

result_directory = '../dataset/temp/BugLocator_test_run'
bug_report_file = '../dataset/aspectj-filtered.xml'
bug_data = get_bug_data(bug_report_file, result_directory)

for top in range(5,11,5):
    count = 0
    total_bug = 0
    for current_bug_data in bug_data:
        # print(current_bug_data['bug_id'])
        suspicious_files = current_bug_data['suspicious_files'].split(",")
        # print(suspicious_files)
        fixed_files = current_bug_data['files'].split(".java ")
        length_of_fixed_files = len(fixed_files)
        fixed_files[length_of_fixed_files-1] = fixed_files[length_of_fixed_files-1].replace('.java','')
        # print(fixed_files) 
        for fixed_file in fixed_files:
            # print(suspicious_files[0:(top+1)])
            if fixed_file + '.java' in suspicious_files[0:top]:
                print(current_bug_data['bug_id'],fixed_file)
                count = count + 1
                break
        total_bug = total_bug + 1
    print('accuracy@', top, count, total_bug, (count*100/total_bug))