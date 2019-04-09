import requests
from datetime import datetime, timedelta

GITHUB_API_SEARCH_URL = 'https://api.github.com/search/repositories'
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
    resp = requests.get(GITHUB_API_SEARCH_URL, params=params)
    return resp.json()['items']

if __name__ == '__main__':
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
            rep['open_issues'],
        )
        print(rep_info)
