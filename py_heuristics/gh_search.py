import re, urllib2, time
from github import Github

access_token = 'd05b43a10f8bc3720d6d20f23f2fa3cbff8d8360'
gh = Github(access_token)

def search_repositories(q):
    try:
        repos=gh.search_repositories(query=q)
    except Exception, e:
        return None
    return repos

def downloadWebPage(url_link):
    url_item = None
    try:
        url_item = urllib2.urlopen(url_link)
    except:
        print 'Wrong GitHub URL!'
    if url_item:
        page_bytes = url_item.read()
        page_txt = page_bytes.decode('utf-8', 'ignore')
        ascii_str = page_txt.encode('ascii','ignore')
        return ascii_str
    return None

if __name__ == '__main__':
    DEBUG = True
    min_num_of_commits = 100
    min_num_of_contributors = 2
    if DEBUG:
        total_cnt = 0
    with open('py_apps.txt', 'w') as wf:
        for year in range(2008, 2017+1):
            for month in range(1, 12+1):
                if month == 12:
                    query = "language:Python fork:0 stars:>=10 archived:false pushed:>=2017-06-01 created:%d-12-01..%d-01-01" %(year,year+1)
                else:
                    query = "language:Python fork:0 stars:>=10 archived:false pushed:>=2017-06-01 created:%d-%02d-01..%d-%02d-01" %(year,month,year,month+1)
                repos = search_repositories(query)
                if DEBUG:
                    monthly_cnt = repos.totalCount
                    print '%d-%02d' %(year,month), monthly_cnt
                    time.sleep(1)
                    total_cnt += monthly_cnt
                
                for repo in repos:
                    web_str = downloadWebPage(repo.html_url)
                    if web_str:
                        commits_res = re.findall(r'\<span class\="num text\-emphasized"\>\s+([0-9\,]+)\s+\<\/span\>\s+commits?\s+\<\/a\>', web_str, re.M)
                        if len(commits_res):
                            commit_cnt = int(re.sub(r'\,', '', commits_res[0]))
                            if commit_cnt >= 100:
                                contributors_res = re.findall(r'\<span class\="num text\-emphasized"\>\s+([0-9\,]+)\s+\<\/span\>\s+contributors?\s+\<\/a\>', web_str, re.M)
                                if len(contributors_res):
                                    contributors_cnt = int(re.sub(r'\,', '', contributors_res[0]))
                                    if contributors_cnt >= 2:
                                        print ' ', repo.html_url
                                        wf.write(repo.html_url + '\n')
        if DEBUG:
            print total_cnt
    
    '''with open('py_apps.txt', 'w') as wf:
        for repo in repos:
            print repo
            web_str = downloadWebPage(repo.html_url)
            if web_str:
                commits_res = re.findall(r'\<span class\="num text\-emphasized"\>\s+([0-9\,]+)\s+\<\/span\>\s+commits?\s+\<\/a\>', web_str, re.M)
                if len(commits_res):
                    commit_cnt = int(re.sub(r'\,', '', commits_res[0]))
                    if commit_cnt >= 100:
                        contributors_res = re.findall(r'\<span class\="num text\-emphasized"\>\s+([0-9\,]+)\s+\<\/span\>\s+contributors?\s+\<\/a\>', web_str, re.M)
                        if len(contributors_res):
                            contributors_cnt = int(re.sub(r'\,', '', contributors_res[0]))
                            if contributors_cnt >= 2:
                                print ' ', repo.html_url
                                wf.write(repo.html_url + '\n')'''
                
