#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 9:23 PM
# @Author  : Agonsle
# @Site    : 
# @File    : cloud.py
# @Software: PyCharm
import regex as re

import jieba
import wordcloud

f = open('../spider/bilibili/alldanmu.csv', encoding='utf-8')
txt = f.read()
danmus = txt.split('\n')
danmus = [x.split(",")[-1] for x in danmus[1:]]
txt = ""
for danmu in danmus:
    txt += danmu + " "

emo_pattern = re.compile(r'\[.*?]')  # 过滤评论和弹幕里的表情 如[doge] [吃瓜]
url_pattern = re.compile("https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # 过滤评论里分享的url

emos = emo_pattern.findall(txt)  # pattern.sub结果不对 用了很笨很慢的方法代替
url = url_pattern.findall(txt)
url.append("哔哩哔哩")
for emo in (emos + url):
    txt = txt.replace(emo, "")

# print(txt)
s = ''.join(jieba.lcut(txt))
wc = wordcloud.WordCloud(width=700, height=700, background_color='white', font_path='C:/Windows/Fonts/simsun.ttc',
                         scale=15)
wc.generate(s)
wc.to_file("../draw/wc_danmu.png")
