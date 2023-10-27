import os
import pandas as pd
from github import Github, Issue
from datetime import datetime, timedelta

import load_data


def update_weather_csv():
    station_info = pd.read_csv('./input/종관기상_관측지점.csv')

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")

    current_year = datetime.now().year
    for idx, row in station_info.iterrows():
        stn_id = row['지점코드']
        filename = f'./output/weather/{stn_id}_{current_year}.csv'
        if os.path.exists(filename):
            update_weather = load_data.request_weather_api(stn_id, yesterday)
            exists_weather = pd.read_csv(filename)
            update_weather = pd.concat([exists_weather, update_weather], ignore_index=True)
            update_weather = update_weather.drop_duplicates()
            update_weather.to_csv(filename, index=False)


def update_price_csv():
    filename = './output/price_data.csv'

    today = datetime.now()
    today = today.strftime("%Y%m%d")

    current_data = load_data.request_price_api(today)

    past_data = pd.read_csv(filename)

    update_data = pd.concat([past_data, current_data], ignore_index=True)
    update_data.to_csv(filename, index=False)

    return current_data

def update_price_issue(current_data):
    today = datetime.now()

    title = f'{today.strftime("%Y%m%d")} - 서울 채소류 소매 가격 정보'
    GITHUB_TOKEN = os.environ['MY_GITHUB_TOKEN']
    REPO_NAME = 'Action_API'
    repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
    body = current_data

    if REPO_NAME == repo.name:
        if not body.empty:
            table_md = '| ' + ' | '.join(body.columns) + ' |\n'
            table_md += '| ' + ' | '.join(['---'] * len(body.columns)) + ' |\n'

            for index, row in body.iterrows():
                table_md += '| ' + ' | '.join([str(cell) for cell in row]) + ' |\n'

            body = table_md
        else:
            body = '데이터가 없습니다.'

        repo.create_issue(title=title, body=body)

def main():
    current_data = update_price_csv()
    update_weather_csv()
    update_price_issue(current_data)

if __name__ == '__main__':
    main()
