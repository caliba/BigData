#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 9:54 PM
# @Author  : Agonsle
# @Site    : 
# @File    : bilibili_comment.py
# @Software: PyCharm
import os
import pandas as pd
import requests
max_page = 10
file_name = 'comments_bi.csv'


def geturl(page):
    url = f"https://api.bilibili.com/x/v2/reply/main?csrf=48cfbcf22e6ef3b1f566ec1064b231e0&mode=3&next={page}&oid=215631694&plat=1&type=1"
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    r = requests.get(url=url,headers=headers)
    r.encoding = 'utf-8'
    text = r.json()['data']['replies']
    print("page  "+str(page))
    return text

def getData():
    for page in range(1,max_page+1):
        text = geturl(page)
        comment_list = []
        user_name = []
        for t in text:
            comment_list.append(t['content']['message'])
            user_name.append(t['member']['uname'])
        df = pd.DataFrame({
            '用户': user_name,
            '评论内容': comment_list
        })
        if os.path.exists(file_name):
            header = False
        else:
            header = True
        df.to_csv(file_name, mode='a+', index=False, header=header, encoding='utf_8_sig')


def main():
    getData()

if __name__ == '__main__':
    main()
