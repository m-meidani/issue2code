import json
import requests

def get_commits(owner,repo):
    r = requests.get('https://api.github.com/repos/%s/%s/commits' % (owner, repo))
    repos = json.loads(r.content)
    for repo in repos:
        commit_id = repo['url'].split('commits')[1]
        print(commit_id)
        a_list = repo['commit']['message'].split('#',1)
        if len(a_list) == 2:
            if not a_list[1].isdigit():
                print (a_list[1].split('\n')[0])
            else:
                print (a_list[1])
        r = requests.get(repo['url'])
        commit = json.loads(r.content)
        file_name = commit['files']
        for c in file_name:
            print(c['filename'])

get_commits('etlegacy','etlegacy')