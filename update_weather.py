import os
import tqdm
import time
import pytz
import pandas as pd
from datetime import datetime, timedelta

import load_data

desired_timezone = pytz.timezone('Asia/Seoul')

def save_check():
    pass

def update_weather():
    station_info = pd.read_csv('./input/관측지점코드.csv')
    station_dct = dict(zip(station_info['지점명'], station_info['지점']))

    today = datetime.now(desired_timezone)
    d = (today - timedelta(days=1)).strftime('%Y%m%d')
    y = d[0:4]
    m = d[4:6]

    for name, code in tqdm.tqdm(station_dct.items()):
        file_dir = f'./data_weather/{name}/{y}'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_path = os.path.join(file_dir, f'{m}.csv')

        check_flag = 0
        max_retries = 3

        while check_flag == 0 and max_retries > 0:
            d_df = load_data.request_weather_api(code, d, d)

            if not d_df.empty:
                if os.path.exists(file_path):
                    e_df = pd.read_csv(file_path)
                    u_df = pd.concat([e_df, d_df], ignore_index=True)
                    u_df.to_csv(file_path, index=False)
                else:
                    d_df.to_csv(file_path, index=False)

                check_flag = 1
            else:
                max_retries -= 1
                time.sleep(1)

def main():
    update_weather()

if __name__ == '__main__':
    main()
