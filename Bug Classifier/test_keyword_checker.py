import re
import csv
from bug_data_retriever import get_bug_data


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
output_file = 'keywords/keyword-' + project + '.csv'
bugs = get_bug_data(xml_path)

keywords = ['test','build']
counter = 0
with open(output_file, 'a', newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['bug_id','decision'])
    for bug in bugs:
        found = False
        # print(bug['bug_id'])
        content = str(bug['summary'] or '')+ ' ' + str(bug['description'] or '')
        tokens = tokenize_bug_report(content)
        for keyword in keywords:
            if keyword  in tokens:
                writer.writerow([bug['bug_id'],"found"])
                counter = counter + 1
                found = True
                break
        if found == False:
            writer.writerow([bug['bug_id'],"not-found"])

print('total match', counter)