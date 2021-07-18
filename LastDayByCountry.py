import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json


# 采集最近一日各国疫情数据
class CoronaVirusSpider(object):

    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def get_content_from_url(self, url):
        """
        根据url,获取响应内容的字符串数据
        :param url :请求url
        :return: 响应内容的字符串
        """
        response = requests.get(url)
        return response.content.decode()

    def parse_home_page(self, index, tag):
        """
        解析首页内容，获取Python数据
        :param index:首页内容
        :return: 解析后的Python数据
        """
        soup = BeautifulSoup(index, 'lxml')
        script = soup.find(id=tag)
        text = script.string
        json_str = re.findall(r'\[.+]', text)[0]
        data = json.loads(json_str)
        return data

    def save_to_json(self, data, path):

        if os.path.exists('data'):
            with open(path, 'w', encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False)
        else:
            os.mkdir('data')
            with open(path, 'w', encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False)

    def save_to_excel(self, json_file, excel_file):
        df = pd.read_json(json_file, encoding='UTF-8')  # 如果文本里有汉字格式，此处需要设置encoding= 'UTF-8'，否则汉字会乱码
        df.to_excel(excel_file, index=False)  # 不要索引

    def last_day_corona_virus(self):
        """
        采集最近一日各国疫情数据
        :return:
        """
        # 1.发送请求，获取首页内容
        home_page = self.get_content_from_url(self.home_url)
        # 2.解析首页内容，获取最近一天的各国疫情数据
        last_day_country_list = self.parse_home_page(home_page, 'getListByCountryTypeService2true')
        # 3.保存数据
        json_file = 'data/last_day_country_data.json'
        excel_file = 'data/last_day_country_data.xlsx'
        self.save_to_json(last_day_country_list, json_file)
        self.save_to_excel(json_file, excel_file)
        print('最近一日各国疫情数据保存成功')

    def run(self):
        self.last_day_corona_virus()


if __name__ == '__main__':
    spider = CoronaVirusSpider()
    spider.run()
