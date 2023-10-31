import os
import pytz
import pandas as pd
from github import Github, Issue
from datetime import datetime, timedelta

import load_data

desired_timezone = pytz.timezone('Asia/Seoul')

def update_weather_csv():
    station_info = pd.read_csv('./input/종관기상_관측지점.csv')

    today = datetime.now(desired_timezone)
    sdate = today - timedelta(days=3)
    edate = today - timedelta(days=1)

    current_year = edate.year


    sdate = sdate.strftime("%Y%m%d")
    edate = edate.strftime("%Y%m%d")


    for idx, row in station_info.iterrows():
        stn_id = row['지점코드']
        filename = f'./output/weather/{stn_id}_{current_year}.csv'

        if os.path.exists(filename):
            update_weather = load_data.request_weather_api(stn_id, sdate, edate)
            exists_weather = pd.read_csv(filename)
            update_weather = pd.concat([exists_weather, update_weather], ignore_index=True)
            update_weather = update_weather.drop_duplicates()
            update_weather.to_csv(filename, index=False)
        # else:
        #     update_weather = load_data.request_weather_api(stn_id, yesterday)
        #     update_weather.to_csv(filename, index=False)


def update_price_csv(code, value):

    today = datetime.now(desired_timezone)
    today_weekday = today.weekday()
    current_year = today.year

    today = today.strftime("%Y%m%d")

    filename = f"./output/price/{value}_{current_year}.csv"

    try:
        current_data = load_data.request_price_api(today, code)
        if os.path.exists(filename) and today_weekday != 6:
            past_data = pd.read_csv(filename)
            update_data = pd.concat([past_data, current_data], ignore_index=True)
            update_data = update_data.drop_duplicates()
            update_data.to_csv(filename, index=False)
        else:
            current_data.to_csv(filename, index=False)

        return current_data

    except:
        pass

def update_price_issue(current_data, value):
    today = datetime.now(desired_timezone)

    title = f'전국 소매 가격 정보 - {today.strftime("%Y%m%d")}'
    GITHUB_TOKEN = os.environ['MY_GITHUB_TOKEN']
    REPO_NAME = 'Action-API'
    repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
    body = current_data

    def add_comment_to_issue(repo, issue_number, comment):
        issue = repo.get_issue(issue_number)
        issue.create_comment(comment)

    if REPO_NAME == repo.name:
        if body is not None and not body.empty:
            table_md = '| ' + ' | '.join(body.columns) + ' |\n'
            table_md += '| ' + ' | '.join(['---'] * len(body.columns)) + ' |\n'

            for index, row in body.iterrows():
                table_md += '| ' + ' | '.join([str(cell) for cell in row]) + ' |\n'

            body = f"### {value}\n" + table_md
        else:
            body = f"### {value}\n" + '데이터가 없습니다.'

        existing_issue = None
        for issue in repo.get_issues():
            if issue.title == title:
                existing_issue = issue
                break

        if existing_issue:
            add_comment_to_issue(repo, existing_issue.number, body)
        else:
            repo.create_issue(title=title, body=body)

def main():

    code_dict = {100: '식량작물', 200: '채소류', 300: '특용작물', 400: '과일류', 500: '축산물', 600: '수산물'}
    for code, value in code_dict.items():
        current_data = update_price_csv(code, value)
        # update_price_issue(current_data, value)

    update_weather_csv()

if __name__ == '__main__':
    main()
