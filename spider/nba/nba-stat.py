#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 10:55 AM
# @Author  : Agonsle
# @Site    : 
# @File    : nba-stat.py
# @Software: PyCharm

import os.path
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

file_path = 'nba_stat.csv'
number_count = []
name_count = []
out_list = []


def geturl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',

    }
    # url = 'http://www.stat-nba.com/query.php?crtcol=fga&order=1&page=0&QueryType=all&AllType=season&AT=tot'
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    # print(res.text)
    return soup


def getData():
    for i in range(100):
        url = 'http://www.stat-nba.com/query.php?crtcol=fga&order=1&page={}&QueryType=all&AllType=season&AT=tot'.format(
            i)
        soup = geturl(url)
        a = 0
        for item in soup.find_all('td'):
            # print(str(item))
            if a % 25 == 0:
                data = re.findall('<td class=".*?">(.*?)</td>', str(item))
                number_count.append(data[0])
            if a % 25 == 1:
                data = re.findall('<td class=".*?">(.*?)</td>', str(item))
                # <a class="query_player_name" href="./player/136.html" target="_blank">卡里姆-贾巴尔</a>
                data1 = re.findall('<a class=".*?" href=".*?">(.*?)</a>', data[0])
                # print(data1)
                name_count.append(data1[0])
            if a % 25 == 6:
                data = re.findall('<td class=".*?">(.*?)</td>', str(item))
                # print(data[0])
                out_list.append(data[0])

            a = a + 1


def main():
    getData()
    df = pd.DataFrame({
        '排名': number_count,
        '球员名': name_count,
        '出手数': out_list,
    })
    if os.path.exists(file_path):
        header = None
    else:
        header = ['排名', '球员名', '出手数']
    df.to_csv(file_path, mode='a+', index=False, header=header, encoding='utf_8_sig')



if __name__ == '__main__':
    main()
