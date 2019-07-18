import re, urllib2
import time
from github import Github

access_token = '[access_token]'
gh = Github(access_token)


def search_repositories(q):
    try:
        repos = gh.search_repositories(query=q)
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
        ascii_str = page_txt.encode('ascii', 'ignore')
        return ascii_str
    return None


if __name__ == '__main__':
    # q = "language:Python fork:0 stars:>5"
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # Conditions:
    language = 'Python'
    min_forks = 0
    min_commits = 20
    min_contributors = 2
    q = "language:%s fork:%d" % (language, min_forks)
    repos = search_repositories(q)
    print 'repo in total : %d'%(len(list(repos)))
    final_repos = []
    with open('py_appttts_l%s_f%d_Com%d_Con%d.txt' % (language,min_forks,min_commits,min_contributors), 'w') as wf:
        for repo in repos:
            print repo
            web_str = downloadWebPage(repo.html_url)
            if web_str:
                commits_res = re.findall(
                    r'\<span class\="num text\-emphasized"\>\s+([0-9\,]+)\s+\<\/span\>\s+commits?\s+\<\/a\>', web_str,
                    re.M)
                if len(commits_res):
                    commit_cnt = int(re.sub(r'\,', '', commits_res[0]))
                    if commit_cnt >= min_commits:
                        contributors_res = re.findall(
                            r'\<span class\="num text\-emphasized"\>\s+([0-9\,]+)\s+\<\/span\>\s+contributors?\s+\<\/a\>',
                            web_str, re.M)
                        if len(contributors_res):
                            contributors_cnt = int(re.sub(r'\,', '', contributors_res[0]))
                            if contributors_cnt >= min_contributors:
                                print ' ', repo.html_url
                                wf.write(repo.html_url + '\n')
            # print re.findall(r'\<span class\="num text\-emphasized"\>\n\s+([0-9]+)\n\s+\<\/span\>\n\s+commits', repo.html_url, re.M)
            '''num_of_commits = len(list(repo.get_commits()))
            num_of_contributors = len(list(repo.get_contributors()))
            if num_of_commits > min_num_of_commits and num_of_contributors > min_num_of_contributors:
                final_repos.append(repo)
                print 'name:', repo.name
                print '  html_url:', repo.html_url
                print '  url:', repo.url
                print '  #commits:', num_of_commits
                print '  #contributors:', num_of_contributors
                wf.write(repo.html_url + '\n')'''
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
