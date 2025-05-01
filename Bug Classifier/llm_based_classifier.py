import os
import csv
import json
from bug_data_retriever import get_bug_data
from openai import OpenAI

client = OpenAI(
    api_key="**",
)


def extract_filename(fully_qualified_path):
    return os.path.basename(fully_qualified_path)

def ask_gpt(content, filenames):
    prompt = f"""
    Given the bug report, determine whether any of the provided filenames are explicitly mentioned in the bug report text.
    
    Only consider filenames as mentioned if their full name or a significant, unambiguous part of the filename (such as a class name without the full package path) appears exactly in the bug report.
    
    If none of the filenames appear exactly, return "no_file". Otherwise, return the matched filenames.

    Bug report: {content}
    Filenames: {filenames}
    """

    # print(prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise file name detector."},
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema", 
                "json_schema": {
                "name": "output_format",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "filename_mentioned": {
                            "type": "string",
                            "description": "filenames mentioned in the bug report",
                        }
                    },
                    "required": ["filename_mentioned"],
                    "additionalProperties": False
                }
            }},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"API error: {e}")
        return {"filename_mentioned": False}

project = 'jdt'
xml_path = '../../dataset/' + project + '-merged.xml'
output_file = 'llm-based-' + project + '.csv'
bugs = get_bug_data(xml_path)

count = 1
with open(output_file, 'a', newline="") as csv_file:
    writer = csv.writer(csv_file)
    # writer.writerow(['bug_id','fixed_file','decision'])
    for bug in bugs:
        # print(bug['bug_id'])
        if bug['bug_id']=="133481":
            content = str(bug['summary'] or '')+ ' ' + str(bug['description'] or '')
            
            fixed_files = bug['fixed_files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            fixed_files = [extract_filename(file) for file in fixed_files]

            response = ask_gpt(content, fixed_files)
            # print(response)
            filename_mentioned = response.get("filename_mentioned", "no_file")

            if filename_mentioned == "no_file":
                writer.writerow([bug['bug_id'],"N/A","not-localizable"])
            else:
                writer.writerow([bug['bug_id'],filename_mentioned, "localizable"])
            break
        count = count + 1
        # break
