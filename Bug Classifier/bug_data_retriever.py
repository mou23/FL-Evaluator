import xml.etree.ElementTree as ET

def get_bug_data(xml_path):
    bugs = []
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for element in root.findall(".//table"):
        bug_id = element[1].text
        summary = element[2].text
        description = element[3].text
        fixed_commit_time = element[8].text
        fixed_files = element[9].text
        buggy_commit = element[10].text
        buggy_commit_time = element[11].text
        
        bug_data = {"bug_id": bug_id,
                    "summary": summary,
                    "description": description,
                    "previous_commit": buggy_commit,
                    "previous_commit_time": buggy_commit_time,
                    "fixed_commit_time": fixed_commit_time, 
                    "fixed_files": fixed_files}
        bugs.append(bug_data)

    bugs = sorted(bugs, key=lambda d: d['fixed_commit_time'])

    length = len(bugs)
    # print('total bugs', length)
    starting_index = length - int(length*0.4)
    latest_bugs = bugs[starting_index:length]
    
    # print(new_bugs)

    latest_bugs = sorted(latest_bugs, key=lambda d: d['previous_commit_time'])
    
    return latest_bugs