import os
import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urlencode

def request_price_api(date, code):
    url = 'http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList'
    p_cert_key = os.environ['PRICE_API_KEY']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
                             'Safari/537.36'}

    params = f'&{quote_plus("p_cert_key")}={p_cert_key}&' + urlencode({
        quote_plus("p_cert_id"): "3749",
        quote_plus("p_returntype"): "json",
        quote_plus("p_product_cls_code"): "01",
        quote_plus("p_item_category_code"): f"{code}",
        quote_plus("p_regday"): date,
        quote_plus("p_convert_kg_yn"): 'N',
    })

    try:
        result = requests.get(url + params, headers=headers)
    except:
        time.sleep(2)
        result = requests.get(url + params, headers=headers)

    try:
        js = json.loads(result.content)
        each_data = pd.DataFrame(js['data']['item'])
        each_data['date'] = date
        return each_data

    except:
        pass


def request_weather_api(stn_Ids, s_d, e_d):
    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    servicekey = 'HOhrXN4295f2VXKpOJc4gvpLkBPC/i97uWk8PfrUIONlI7vRB9ij088/F5RvIjZSz/PUFjJ4zkMjuBkbtMHqUg=='

    # servicekey = os.environ['WEATHER_API_KEY']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
                             'Safari/537.36'}

    params = f'?{quote_plus("ServiceKey")}={servicekey}&' + urlencode({
        quote_plus("pageNo"): "1",  # 페이지 번호 // default : 1
        quote_plus("numOfRows"): "720",  # 한 페이지 결과 수 // default : 10
        quote_plus("dataType"): "JSON",  # 응답자료형식 : XML, JSON
        quote_plus("dataCd"): "ASOS",
        quote_plus("dateCd"): "DAY",
        quote_plus("startDt"): s_d,
        quote_plus("endDt"): e_d,
        quote_plus("stnIds"): f"{stn_Ids}"
    })
    try:
        result = requests.get(url + params, headers=headers)
    except:
        time.sleep(3)
        result = requests.get(url + params, headers=headers)

    try:
        js = json.loads(result.content)
        df = pd.DataFrame(js['response']['body']['items']['item'])
        df['tm'] = pd.to_datetime(df['tm'])
        df['year'] = df['tm'].dt.year
        df['month'] = df['tm'].dt.month
        df['day'] = df['tm'].dt.day

        cols = ['year', 'month', 'day', 'avgTa', 'minTa', 'maxTa', 'sumRn', 'sumSsHr', 'ddMefs']

        df = df[cols]
        df.columns = ['year', 'month', 'day', 'tavg', 'tmin', 'tmax', 'rain', 'sunshine', 'snow']

        return df
    except:
        pass

