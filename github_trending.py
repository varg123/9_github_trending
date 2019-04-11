import requests
from datetime import datetime, timedelta

COUNT_REPOSITORIES = 20
DAYS_DELTA = 7


def get_trending_repositories(top_size, time_delta):
    fmt = '%Y-%m-%d'
    start_date = (datetime.now()-timedelta(days=time_delta)).strftime(fmt)
    params = {
        'q': 'created:>={}'.format(start_date),
        'sort': 'stars',
        'per_page': top_size,
    }
    url_search_api = 'https://api.github.com/search/repositories'
    resp = requests.get(url_search_api, params=params)
    return resp.json()['items']


def get_open_issues(repos_url):
    page = 1
    while True:
        params = {
            'state': 'open',
            'page': page,
            'per_page': 50,
        }
        resp = requests.get(
            '{}/{}'.format(repos_url, '/issues'),
            params=params
        )
        data_issues = resp.json()
        if not data_issues:
            break
        page += 1
        yield from data_issues


def get_open_issues_amount(repos_url):
    amount = 0
    for issue in get_open_issues(repos_url):
        if 'pull_request' not in issue:
            amount += 1
    return amount


def main():
    repositories = get_trending_repositories(COUNT_REPOSITORIES, DAYS_DELTA)
    tmpl = '''
    Имя: {}
    Звёзд: {}
    Описание: {}
    Ссылка: {}
    Открытых проблемм: {}
    '''
    for rep in repositories:
        rep_info = tmpl.format(
            rep['name'],
            rep['stargazers_count'],
            rep['description'],
            rep['html_url'],
            get_open_issues_amount(rep['url']),
        )
        print(rep_info)

if __name__ == '__main__':
    main()
