import os
import pytz
import pandas as pd
from github import Github, Issue
from datetime import datetime, timedelta

import load_data

desired_timezone = pytz.timezone('Asia/Seoul')


def update_price_csv(code, value, date):

    today = date
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

def main():

    today = datetime.now(desired_timezone)
    today = today - timedelta(days=1)


    code_dict = {100: '식량작물', 200: '채소류', 300: '특용작물', 400: '과일류', 500: '축산물', 600: '수산물'}
    for code, value in code_dict.items():
        current_data = update_price_csv(code, value, today)


if __name__ == '__main__':
    main()
