import os
import base64
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    data_dir = './output/weather'

    station_info = pd.read_csv('./input/종관기상_관측지점.csv')
    location_dict = dict(zip(station_info['지점명'], station_info['지점코드']))

    location_list = list(location_dict.keys())

    selected_location = st.selectbox('지역 선택', location_list)

    year_list = [2023,]
    selected_year = st.selectbox('연도 선택', year_list)

    df = pd.read_csv(os.path.join(data_dir, f'{location_dict[selected_location]}_{selected_year}.csv'))
    df['year'] = pd.to_datetime(df['tm']).dt.year
    df['month'] = pd.to_datetime(df['tm']).dt.month
    df['day'] = pd.to_datetime(df['tm']).dt.day

    df_pivot = df.pivot_table(index='month', columns='day', values='avgTa')

    fig = plt.figure(figsize=(20, 8))
    ax = sns.heatmap(df_pivot, cmap='coolwarm', linewidths=1, square=True, annot=True)
    st.pyplot(fig)

    df = df.drop(["day", "month", "year"], axis=1)

    if st.button("Download CSV"):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
