import os
import pytz
import pandas as pd
from github import Github, Issue
from datetime import datetime, timedelta

import load_data

desired_timezone = pytz.timezone('Asia/Seoul')

def update_price_csv(code, date):

    today = date
    today = today.strftime("%Y%m%d")


    try:
        current_data = load_data.request_price_api(today, code)
        current_data = current_data[['item_name','kind_name','rank','unit','day1','dpr1']]
        return current_data

    except:
        pass

def update_price_issue(current_data, value):
    today = datetime.now(desired_timezone)
    today = today - timedelta(days=1)

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
    today = datetime.now(desired_timezone)
    today = today - timedelta(days=1)

    code_dict = {100: '식량작물', 200: '채소류', 300: '특용작물', 400: '과일류', 500: '축산물', 600: '수산물'}
    for code, value in code_dict.items():
        current_data = update_price_csv(code, today)
        update_price_issue(current_data, value)


if __name__ == '__main__':
    main()
