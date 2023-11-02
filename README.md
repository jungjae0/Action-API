# 기상/농산물가격정보 API + GitHub Action

## Settings

### API Key 발급

| 구분                    | 제공                 | link                                                               |
|-----------------------|--------------------|--------------------------------------------------------------------|
| 지상(종관, ASOS) 일자료 조회서비스 | 기상청(공공데이터 포털)      | [link](https://www.data.go.kr/data/15059093/openapi.do)            |
| 농산물 가격 정보             | 한국농수산식품유통공사(KAMIS) | [link](https://www.kamis.or.kr/customer/reference/openapi_list.do) |


### GitHub Token 발급

Settings / Developer Settings / Personal access tokens / Tokens(classic)

![GitHub Token](https://github.com/jungjae0/Action-API/assets/93760723/2163c604-9744-4db7-8b7d-c8091ef269ee)

### Actions secrets and variables

Repository Settings / Secrets and variables / Actions / New repository secret

API Key, GitHub Token 등록

![Secrets Keys](https://github.com/jungjae0/Action-API/assets/93760723/a39dc6b7-1b88-40d5-9a48-a75d1dd80940)

```yaml
# workflows/update_data.yml
- name: Run Python Script
  run: python update_data.py
  env:
    MY_GITHUB_TOKEN: ${{ secrets.MY_GITHUB_TOKEN }}
    PRICE_API_KEY: ${{ secrets.PRICE_API_KEY }}
    WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
```

```python
# load_data.py
p_cert_key = os.environ['PRICE_API_KEY']
servicekey = os.environ['WEATHER_API_KEY']

# update_data.py
GITHUB_TOKEN = os.environ['MY_GITHUB_TOKEN']
```

## Results


**매일 새벽 1시 업데이트**

| 구분   | 일별 기상 데이터 streamlit                                                                                       | 일별 부류별 농산물 도.소매 가격 정보                                                                                 |
|------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| link | **[link](https://actionapi.streamlit.app/)**                                                              | **[link](https://github.com/jungjae0/Action-API/issues)**                                                 |
| data | **[link](./output/weather)**                                                                              | **[link](./output/price)**                                                 |
| 결과   | ![streamlit](https://github.com/jungjae0/Action-API/assets/93760723/80565b6b-dfaf-4005-a31c-be0d67ad8eb5) | ![issue](https://github.com/jungjae0/Action-API/assets/93760723/6f6e6c64-7c74-456a-8cd1-1a4b845aeab2) |



-----

1. ```load_data.py``` > request API
2. ```update_data.py``` > update csv/issue

    - ```update_issue.py``` > update issue
    - ```update_price.py``` > update price
    - ```update_weather.py``` > update weather

3. ```.github/workflows/update_data.yml``` > GitHub Action workflow
4. ```app.py``` > temperature monitoring streamlit app
5. ```output``` > update data
