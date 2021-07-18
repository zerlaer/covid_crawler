import json

import pandas as pd
import re
import xlwt

excel = pd.read_excel('data/last_day_china_data.xlsx')
df = pd.DataFrame(excel)
areas = df['dangerAreas']

for area in areas:
    if area != "[]":
        area = str(area).split('""')
        sa = pd.Series(area)
        sa.to_csv('data/全国疫情风险就地区汇总.csv',index=None,header=None)
df.drop(df.columns[[0, 7, 8, 9, 10, 11, 12, 13, 14, 15]], axis=1, inplace=True)
da = df.rename(columns={'provinceShortName': '地区', 'currentConfirmedCount': '现存确诊', 'confirmedCount': '累计确诊',
                                  'suspectedCount': '疑似病例', 'curedCount': '治愈', 'deadCount': '死亡人数'})
da.to_excel('data/全国最新疫情数据.xlsx',index=None)

