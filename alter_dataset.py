import sys
import csv
import os
import random
csv.field_size_limit(sys.maxsize)


def alter_dataset(project_path, dataset_file, output_file, repo, extensions):
    # Find list of interested files
    list_of_files = []
    for path, subdirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(tuple(extensions)):
                list_of_files.append(os.path.join(path, file))

    # Separate issue related data from dataset to reduce data duplication
    issues = {}
    files = []
    with open(dataset_file, 'r') as csv_in:
        reader = csv.DictReader(x.replace('\0', '') for x in csv_in)
        for row in reader:
            if row['issue'] not in issues:
                issues[row['issue']] = {
                    'id': row['issue'],
                    'title': row['issue_title'],
                    'body': row['issue_body'],
                    'files': []
                }

            # Filter non-source files
            if row['filename'].endswith(tuple(extensions)):
                issues.get(row['issue']).get('files').append(row['filename'])
                files.append({
                    'filename': row['filename'],
                    'file_content': row['file_content'],
                    'issue': row['issue'],
                    'related': row['related']
                })

    # Add additional non-related files to the file dataset:
    for issue in issues:
        non_related_files = []
        # We add non_related files 2 times more than related ones
        while len(non_related_files) < len(issues[issue].get('files')) * 2:
            file = random.choice(list_of_files)
            if file not in issues[issue].get('files'):
                non_related_files.append(file)

        # Read the content and add to dataset
        for item in non_related_files:
            with open(item, 'rb') as file_in:
                files.append({
                    'filename': item[item.rindex('/')+1:],
                    'file_content': file_in.read().decode('utf-8', errors="ignore"),
                    'issue': issue,
                    'related': False
                })
    # Write issue related data
    with open('./filtered_data/issues_data_{}.csv'.format(repo), 'w') as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=['id', 'title', 'body'], extrasaction='ignore')
        writer.writeheader()
        for key in issues:
            writer.writerow(issues[key])

    # Write file related data
    with open('./filtered_data/file_data_{}.csv'.format(repo), 'w') as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=['filename', 'file_content', 'issue', 'related'])
        writer.writeheader()
        writer.writerows(files)




p_path = sys.argv[1]
d_path = sys.argv[2]
o_file = sys.argv[3]
repo_name = sys.argv[4]
ext = sys.argv[5]
alter_dataset(p_path, d_path, o_file, repo_name, ext.split(','))