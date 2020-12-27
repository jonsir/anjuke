#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import json
import time
import pandas as pd
from xpinyin import Pinyin
import copy
import argparse


class dataset:
    def getInfo(self, page, fh, area, areapy):

        url = 'https://shanghai.anjuke.com/community/' + areapy + '/p' + str(page) + '/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https: // wuhan.anjuke.com / sale /?from=navigation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60)
        str1 = "万科"
        soup = BeautifulSoup(response.text, 'html.parser')
        information = soup.find_all('div', class_='li-itemmod')
        for i in information:
            infos = i.find_all('div', class_='li-info')
            for info in infos:
                titles = info.find_all('h3')
                for title in titles:
                    strTitle = title.get_text()
            if str1 in strTitle:  # 过滤万科 卡住
                continue
            print(area, page, strTitle)
            li_sides = i.find_all('div', class_='li-side')
            strPrice = 'no price'
            for li_side in li_sides:
                ps = li_side.find_all('p')
                for p in ps:
                    strongs = p.find_all('strong')  # 元/平
                    for price in strongs:
                        strPrice = price.get_text()
                        print(strPrice)
                if strPrice != "":
                    # area,community's name, community's average price
                    fh.write(area.strip() + ',' + strTitle.strip() + ',' + strPrice.strip() + '\n')
                else:
                    continue

    def getlnglat(self, address):
        # get lat,lng
        url = 'http://api.map.baidu.com/geocoder/v2/'

        output = 'json'
        ak = 'dHxEEgwjUsrqManYTG4YBRCDLrGu4DGG'  # api密钥
        add = quote(str(address))
        url_new = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 经纬度

        maxNum = 5
        for i in range(maxNum):
            try:
                req = urlopen(url_new, timeout=60)  # Prevent shielding
            except:
                if i < (maxNum - 1):
                    time.sleep(20)  # wait 20s
                    continue
                else:
                    break

        res = req.read().decode()
        temp = json.loads(res)
        lat = temp['result']['location']['lat']
        lng = temp['result']['location']['lng']
        return lat, lng

    def writelnglat(self, address, fh):
        for i in address.iloc[:, 1]:
            address2 = "上海" + i  # 上海+community's name 避免其他地区重名
            try:
                lat, lng = test.getlnglat(address2)

                print(lng, lat)
                # community's name ,lng,lat
                fh.write(i.strip() + ',' + str(lng).strip() + ',' + str(lat).strip() + '\n')
            except KeyError:
                print("Get A Error")

    def getInfo_price(self, file, area, areapy):
        url = 'https://shanghai.anjuke.com/market/' + str(areapy) + '/'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https: // wuhan.anjuke.com / sale /?from=navigation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        price_trend = soup.find_all(name='div', attrs={"class": "trendR"})
        result = []
        for pt in price_trend:
            for i in range(0, 2):  # 最近两个月的房价
                infos = pt.find_all('em', class_='up')[i].text
                result.append(infos)
            file.write(area.strip() + ',' + str(result) + '\n')

    def grab_data_from_downloaded_raw_files(self):
        data1 = pd.read_csv('../data/data_community_local.txt', header=None)
        data2 = pd.read_csv('../data/data_latlng_local.txt', header=None)
        data3 = pd.read_csv('../data/data_area_price_local.txt', header=None)
        return data1, data2, data3

    def grab_data_by_scraping_and_api_requests(self):
        areaname = [
            '杨浦', '徐汇', '静安', '虹口', '黄浦', '长宁'
        ];

        for i in areaname:
            area = str(i)
            areapy = Pinyin()
            areapy = str(areapy.get_pinyin(area, ''))

            data1 = '../data/data_community.txt'
            dataset1 = open(data1, "a")
            for page in range(1, 6):
                test1 = dataset()
                test1.getInfo(page, dataset1, area, areapy)
            dataset1.close()

            data3 = '../data/data_area_price.txt'
            dataset3 = open(data3, "a")
            test3 = dataset()
            test3.getInfo_price(dataset3, area, areapy)
            dataset3.close()

        data2 = "../data/data_latlng.txt"
        dataset2 = open(data2, "a")
        address = pd.read_csv('../data/data_community.txt', header=None)
        test2 = dataset()
        test2.writelnglat(address, dataset2)
        dataset2.close()
        data1 = pd.read_csv('../data/data_community.txt', header=None)
        data2 = pd.read_csv('../data/data_latlng.txt', header=None)
        data3 = pd.read_csv('../data/data_area_price.txt', header=None)
        return data1, data2, data3

    def grab_data_by_scraping_and_api_requests_test(self):
        areaname = [
            '杨浦'
        ];  # for testing, only 1 area

        for i in areaname:
            area = str(i)  # change chinese characters into characters
            areapy = Pinyin()
            areapy = str(areapy.get_pinyin(area, ''))

            data1 = '../data/data_community.txt'
            dataset1 = open(data1, "a")
            for page in range(1, 6):  # The hotest 150 communities in this area
                test1 = dataset()
                test1.getInfo(page, dataset1, area, areapy)
            dataset1.close()

            data3 = '../data/data_area_price.txt'
            dataset3 = open(data3, "a")
            test3 = dataset()
            test3.getInfo_price(dataset3, area, areapy)
            dataset3.close()

        data2 = "../data/data_latlng.txt"
        dataset2 = open(data2, "a")
        address = pd.read_csv('../data/data_community.txt', header=None)
        test2 = dataset()
        test2.writelnglat(address, dataset2)
        dataset2.close()
        data1 = pd.read_csv('../data/data_community.txt', header=None)
        data2 = pd.read_csv('../data/data_latlng.txt', header=None)
        data3 = pd.read_csv('../data/data_area_price.txt', header=None)
        return data1, data2, data3

    def add_data_to_my_data_model(self, data_community, data_latlng, data_price):
        data_latlng['id'] = range(len(data_latlng))
        data_latlng.rename(columns={0: 'name', 1: 'lng', 2: 'lat'}, inplace=True)
        data_latlng = data_latlng.drop(['name'], axis=1)
        data_latlng.reindex(['id', 'lng', 'lat'], fill_value=range(len(data_latlng)))

        data_community['id'] = range(len(data_community))
        data_community.rename(columns={0: 'area', 1: 'name', 2: 'price'}, inplace=True)

        data = pd.merge(data_community, data_latlng, on='id', how='right')

        data.to_csv('../data/result.csv')

        area = copy.copy(data_price.iloc[:, 0])
        for i in range(len(data_price)):
            for j in range(len(data_price.iloc[0, :])):
                data_price.iloc[i][j] = data_price.iloc[i, j][2:7]
            data_price.iloc[i, 0] = area[i]

        data_price.rename(columns={0: 'Area', 1: 'Dec_price', 2: 'Nov_price'}, inplace=True)
        data_price.to_csv('../data/result_price.csv')

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-source", choices=["test", "remote", "local"], nargs=1,
                            help="where data should be gotten from")
        args = parser.parse_args()

        location = args.source

        if location == ['test']:
            data1, data2, data3 = test.grab_data_by_scraping_and_api_requests_test()
            test.add_data_to_my_data_model(data1, data2, data3)
        elif location == ['remote']:
            data1, data2, data3 = test.grab_data_by_scraping_and_api_requests()
            test.add_data_to_my_data_model(data1, data2, data3)
        elif location == ['local']:
            data1, data2, data3 = test.grab_data_from_downloaded_raw_files()
            test.add_data_to_my_data_model(data1, data2, data3)


if __name__ == '__main__':
    test = dataset()
    test.main()

