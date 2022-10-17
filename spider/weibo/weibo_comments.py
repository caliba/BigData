#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 10:26 AM
# @Author  : Agonsle
# @Site    : 爬取关键字相关微博
# @File    : test_weibo.py
# @Software: PyCharm
import os.path
import re
from pprint import pprint
import pandas as pd
import jsonpath
import requests

key_word = 'TES'
weibo_file = 'weibo.csv'
max_page = 4


def geturl(page):
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate, br"
    }
    url = 'https://m.weibo.cn/api/container/getIndex'
    params = {
        'containerid': "100103type=1&q={}".format(key_word),
        'page_type': "searchall",
        "page": page
    }
    return requests.get(url=url, headers=headers, params=params)

def saveData():
    for page in range(1, max_page + 1):
        r = geturl(page)
        cards = r.json()["data"]["cards"]
        text_list = jsonpath.jsonpath(cards, '$..mblog.text')
        dr = re.compile(r'<[^>]+>', re.S)
        text2_list = []
        if not text_list:
            continue
        if type(text_list) == list and len(text_list) > 0:
            for text in text_list:
                text2 = dr.sub('', text)
                text2_list.append(text2)

        author = jsonpath.jsonpath(cards, '$..mblog.user.screen_name')
        repost = jsonpath.jsonpath(cards, '$..mblog.reposts_count')
        comment = jsonpath.jsonpath(cards, '$..mblog.comments_count')
        zan = jsonpath.jsonpath(cards, '$..mblog.attitudes_count')
        # print(author)
        print(zan)
        df = pd.DataFrame({
            '用户': author,
            '转发数': repost,
            '评论数': comment,
            '点赞数': zan,
            '评论': text2_list
        })
        # weibo_file='weibo.csv'
        if os.path.exists(weibo_file):
            header = None
        else:
            header = ['用户', '转发数', '评论数', '点赞数', '评论']
        df.to_csv(weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')


def main():
    if os.path.exists(weibo_file):
        os.remove(weibo_file)
        print("删除完成")
    saveData()


if __name__ == "__main__":
    main()
