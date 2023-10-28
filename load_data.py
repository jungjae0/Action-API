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


def request_weather_api(stn_Ids, date):
    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    servicekey = os.environ['WEATHER_API_KEY']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
                             'Safari/537.36'}

    params = f'?{quote_plus("ServiceKey")}={servicekey}&' + urlencode({
        quote_plus("pageNo"): "1",  # 페이지 번호 // default : 1
        quote_plus("numOfRows"): "720",  # 한 페이지 결과 수 // default : 10
        quote_plus("dataType"): "JSON",  # 응답자료형식 : XML, JSON
        quote_plus("dataCd"): "ASOS",
        quote_plus("dateCd"): "DAY",
        quote_plus("startDt"): date,
        quote_plus("endDt"): date,
        quote_plus("stnIds"): f"{stn_Ids}"
    })
    try:
        result = requests.get(url + params, headers=headers)
    except:
        time.sleep(2)
        result = requests.get(url + params, headers=headers)

    try:
        js = json.loads(result.content)
        weather = pd.DataFrame(js['response']['body']['items']['item'])
        return weather

    except:
        pass