import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm


# 采集1月23日至今各国疫情数据
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

    def parse_corona_virus(self, last_day_corona_virus_of_china, desc):
        #  定义列表，存储各国从1月23日以来的数据
        corona_virus = []
        for country in tqdm(last_day_corona_virus_of_china, desc):
            # 3. 发送请求，获取各国从1月23日至今的json数据
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            # 4. 把json数据转化为python类型的数据，添加到列表中
            statistics_data = json.loads(statistics_data_json_str)['excel']
            for one_day in statistics_data:
                one_day['provinceName'] = country['provinceName']
                if country.get('countryShortCode'):
                    one_day['countryShortCode'] = country['countryShortCode']
            corona_virus.extend(statistics_data)
            # 5. 把json数据保存为.json格式的文件
        return corona_virus

    def load_data(self, path):
        """
        根据路径加载数据
        :param path:
        :return:
        """
        with open(path, encoding='utf-8') as fp:
            data = json.load(fp)
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

    def last_day_corona_virus_of_china(self):
        """
        采集最近一日中国各省疫情数据
        :return:
        """
        # 1.发送请求，获取疫情数据
        home_page = self.get_content_from_url(self.home_url)
        # 2.解析首页内容，获取最近一日中国各省疫情数据
        last_day_china_list = self.parse_home_page(home_page, 'getAreaStat')
        # 3.保存数据
        json_file = 'data/last_day_china_data.json'
        excel_file = 'data/last_day_china_data.xlsx'
        self.save_to_json(last_day_china_list, json_file)
        self.save_to_excel(json_file, excel_file)
        print('最近一日中国各省疫情数据保存成功')


    def from_january_corona_virus_of_china(self):
        """
        采集1月23日至今中国各省疫情数据
        :return:
        """
        # 1. 加载最近一日中国疫情数据
        last_day_corona_virus_of_china = self.load_data('data/last_day_china_data.json')
        corona_virus = self.parse_corona_virus(last_day_corona_virus_of_china, desc='采集1月23日至今中国疫情信息')
        # 2.把json数据保存为.json格式的文件和excel文件
        json_file = 'data/from_january_china_data.json'
        excel_file = 'data/from_january_china_data.xlsx'
        self.save_to_json(corona_virus, json_file)
        self.save_to_excel(json_file, excel_file)
        print('1月23日至今中国疫情数据保存成功')

    def run(self):
        path= 'data/from_january_china_data.json'
        if os.path.exists(path):
            self.from_january_corona_virus_of_china()
        else:
            self.last_day_corona_virus_of_china()
            self.from_january_corona_virus_of_china()




if __name__ == '__main__':
    spider = CoronaVirusSpider()
    spider.run()
