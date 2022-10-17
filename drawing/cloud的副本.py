#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 9:23 PM
# @Author  : Agonsle
# @Site    : 
# @File    : cloud.py
# @Software: PyCharm
import jieba
import wordcloud

f = open('danmu.txt', encoding='utf-8')
txt = f.read()
s = ''.join(jieba.lcut(txt))
wc = wordcloud.WordCloud(width=700,height=700,background_color='white',font_path='PingFang.ttc',scale=15)
wc.generate(s)
wc.to_file("wc.png")
