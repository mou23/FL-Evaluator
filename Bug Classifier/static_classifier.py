import re
import os
import csv
from bug_data_retriever import get_bug_data

def extract_filename(fully_qualified_path):
    return os.path.basename(fully_qualified_path)


def tokenize_bug_report(content):
    # Define the tokenization pattern
    pattern = r"[ \t\n\\:;,!?/(){}[\]\"']+"
    
    # Use the re.split() method to split the string based on the pattern
    tokens = re.split(pattern, content)
    
    # Remove any empty tokens resulting from consecutive separators
    tokens = [token for token in tokens if token]
    
    return tokens

project = 'tomcat'
xml_path = '../../dataset/' + project + '-merged.xml'
output_file = 'static-' + project + '.csv'
bugs = get_bug_data(xml_path)

with open(output_file, 'a', newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['bug_id','fixed_file','decision'])
    for bug in bugs:
        # print(bug['bug_id'])
        content = str(bug['summary'] or '')+ ' ' + str(bug['description'] or '')
        tokens = tokenize_bug_report(content)
        # print(tokens)
        localizable = False
        fixed_files = bug['fixed_files'].split('.java')
        fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
        
        for file in fixed_files:
            filename = extract_filename(file)
            print(filename)
            # filename = filename + '.java'
            if filename in tokens:
                writer.writerow([bug['bug_id'],filename,"localizable"])
                localizable = True
                break
        if localizable == False:
            writer.writerow([bug['bug_id'],"N/A","not-localizable"])
