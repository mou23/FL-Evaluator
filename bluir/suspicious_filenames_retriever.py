import os

def extract_suspicious_file_data_for_a_bug(file_path):
    with open(file_path, 'r') as file:
        suspicious_files = {}
        for line in file:
            parts = line.split()
            similarity_score = parts[1]
            if len(parts) > 2:
                suspicious_file=' '.join(parts[2:])
                suspicious_files[suspicious_file] = similarity_score
        return suspicious_files
    
def extract_suspicious_filenames_for_all_bugs(directory):
    bug_wise_suspicious_filenames = {}

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for file in files:
        file_path = os.path.join(directory, file)
        suspicious_filenames = (extract_suspicious_file_data_for_a_bug(file_path)).keys()
        filename = os.path.basename(file_path)
        filename_without_extension = os.path.splitext(filename)[0]
        bug_wise_suspicious_filenames[filename_without_extension] = suspicious_filenames

    return bug_wise_suspicious_filenames


def extract_suspicious_file_data_for_all_bugs(directory):
    bug_wise_suspicious_file_data = {}

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for file in files:
        file_path = os.path.join(directory, file)
        suspicious_file_data = extract_suspicious_file_data_for_a_bug(file_path)
        filename = os.path.basename(file_path)
        filename_without_extension = os.path.splitext(filename)[0]
        bug_wise_suspicious_file_data[filename_without_extension] = suspicious_file_data

    return bug_wise_suspicious_file_data
