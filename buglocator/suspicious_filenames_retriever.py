import os

def extract_suspicious_filenames_for_a_bug(file_path):
    with open(file_path, 'r') as file:
        suspicious_filenames = []
        for line in file:
            parts = line.split()
            if len(parts) > 2:
                suspicious_filenames.append(' '.join(parts[2:]))
        return suspicious_filenames
    
def extract_suspicious_filenames_for_all_bugs(directory):
    bug_wise_suspicious_filenames = {}
    folders = [f.path for f in os.scandir(directory) if f.is_dir()]
    # print(folders)
    for folder in folders:
        recommended_folder = os.path.join(folder, "recommended")
        if os.path.exists(recommended_folder) and os.path.isdir(recommended_folder):
            files = [f for f in os.listdir(recommended_folder) if os.path.isfile(os.path.join(recommended_folder, f))]
            for file in files:
                file_path = os.path.join(recommended_folder, file)
                suspicious_filenames = extract_suspicious_filenames_for_a_bug(file_path)
                filename = os.path.basename(file_path)
                filename_without_extension = os.path.splitext(filename)[0]
                bug_wise_suspicious_filenames[filename_without_extension] = suspicious_filenames
        else:
            print(f"'recommended' folder not found in {folder}")

    return bug_wise_suspicious_filenames
