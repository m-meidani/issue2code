import sys
import requests
import re
import json
import csv
from pydriller import RepositoryMining
from collections import defaultdict

commit_issue = {}
commit_changes = defaultdict(list)

BASE_URL = 'https://api.github.com'
GET_ISSUE_URL = '/repos/{owner}/{repo}/issues/{issue_number}'

USERNAME = 'm-meidani'
TOKEN = ''

gh_session = requests.session()
gh_session.auth = (USERNAME, TOKEN)

def commits_with_issue_number(rm):
    for commit in rm.traverse_commits():
        ids = re.findall('#(\d+)', commit.msg)
        if ids:
            commit_issue[commit.hash] = ids
            for m in commit.modifications:
                commit_changes[commit.hash].append((m.filename, m.source_code_before))


def save_issues_to_csv(owner, repo):
    rows = []
    i = 0
    for key in commit_issue:
        for issue in commit_issue[key]:
            url = BASE_URL + GET_ISSUE_URL.format(owner=owner, repo=repo, issue_number=issue)
            response = gh_session.get(url)
            response = json.loads(response.content)
            for change in commit_changes[key]:
                try:
                    rows.append([key, change[0], change[1], issue, response['title'], response['body'], True])
                except KeyError:
                    print(response)
        i+=1
    with open('issues_{}.csv'.format(repo), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['commit', 'filename', 'file_content', 'issue', 'issue_title', 'issue_body', 'related'])
        writer.writerows(rows)

repo_path = sys.argv[1]
repo_owner = sys.argv[2]
repo_name = sys.argv[3]

rm = RepositoryMining(repo_path)
commits_with_issue_number(rm)
save_issues_to_csv(repo_owner, repo_name)
