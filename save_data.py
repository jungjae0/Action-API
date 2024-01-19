import os
import pandas as pd
import tqdm
import load_data
import time
output_dir = './output/cache_weather'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def each_save(stnId, stnNm):
    for year in tqdm.tqdm(range(1973, 2025), desc=f'{stnNm}'):
        stn_dir = os.path.join(output_dir, f'{stnNm}')
        if not os.path.exists(stn_dir):
            os.makedirs(stn_dir)
        save_path = os.path.join(stn_dir, f'{year}.csv')

        if not os.path.exists(save_path):
            if year != 2024:
                sd = f'{year}0101'
                ed = f'{year}1231'
            else:
                sd = f'{year}0101'
                ed = f'{year}0116'
            flag = 0
            while flag < 4:
                try:
                    df = load_data.request_weather_api(stnId, sd, ed)
                    df.to_csv(save_path, index=False)
                    time.sleep(3)
                except:
                    # time.sleep(3)
                    flag += 1
                break

            time.sleep(3)

def split_data(stnNm):
    for year in tqdm.tqdm(range(1973, 2025), desc=f'{stnNm}'):
        stn_dir = os.path.join(output_dir, f'{stnNm}')

        save_stn_dir = os.path.join('weather', f'{stnNm}', f'{year}')
        if not os.path.exists(save_stn_dir):
            os.makedirs(save_stn_dir)
        try:
            df = pd.read_csv(os.path.join(stn_dir, f'{year}.csv'))
            for month in list(df['month'].unique()):
                month_df = df[df['month'] == month]
                month_df.to_csv(os.path.join(save_stn_dir, f'{month:02d}.csv'), index=False)
        except:
            continue

def del_empty():
    root_dir = 'weather'
    lst = []
    for region in os.listdir(root_dir):
        region_path = os.path.join(root_dir, region)

        for year in os.listdir(region_path):
            year_path = os.path.join(region_path, year)
            print(year_path)

            files_in_year = os.listdir(year_path)

            if len(files_in_year) == 0:
                lst.append(year_path)
                # os.rmdir(year_path)
    print(lst)
def main():
    # del_empty()
    station_info = pd.read_csv('./input/관측지점코드.csv')
    station_dct = dict(zip(station_info['지점명'], station_info['지점']))
    for stnNm, stnId in station_dct.items():
        # each_save(stnId, stnNm)
        split_data(stnNm)




if __name__ == '__main__':
    main()