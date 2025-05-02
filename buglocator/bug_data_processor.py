import xml.etree.ElementTree as ET
from suspicious_filenames_retriever import extract_suspicious_filenames_for_all_bugs, extract_suspicious_file_data_for_all_bugs


def get_bug_data(xml_path,result_directory):
    bug_wise_suspicious_filenames = extract_suspicious_filenames_for_all_bugs(result_directory)
    bug_ids = list(bug_wise_suspicious_filenames.keys())
    bugs = []
    
    print(bug_ids)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for table in root.findall(".//table"):
        bug_data = {}
        for column in table.findall(".//column"):
            column_name = column.get("name")
            column_value = column.text
            bug_data[column_name] = column_value
            if(column_name=='bug_id'):
                if(column_value in bug_ids):
                    list_of_suspicious_filenames = bug_wise_suspicious_filenames[column_value]
                    bug_data['suspicious_files'] = ','.join(list_of_suspicious_filenames)
                    bugs.append(bug_data)
    # print(bugs)
    return bugs


def get_bug_data_with_similarity_score(xml_path,result_directory):
    bug_wise_suspicious_file_data = extract_suspicious_file_data_for_all_bugs(result_directory)
    bug_ids = list(bug_wise_suspicious_file_data.keys())
    bugs = []
    
    print(bug_ids)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for table in root.findall(".//table"):
        bug_data = {}
        for column in table.findall(".//column"):
            column_name = column.get("name")
            column_value = column.text
            bug_data[column_name] = column_value
            if(column_name=='bug_id'):
                if(column_value in bug_ids):
                    bug_data['suspicious_file_data'] = bug_wise_suspicious_file_data[column_value]
                    bugs.append(bug_data)
    # print(bugs)
    return bugs