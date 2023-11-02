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

def main():
    update_weather_csv()

if __name__ == '__main__':
    main()
