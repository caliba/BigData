#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 8:32 PM
# @Author  : Agonsle
# @Site    : 爬取b站弹幕（有数量限制）bv --> cid -->danmu
# @File    : bilibili_danmu.py
# @Software: PyCharm
import os.path
import re
import time
import requests
import pandas as pd

bid = 'BV1Dy4y1g7EU'
file_path = 'bilibili_danmu.csv'

def get_cid(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp' % bvid
    res = requests.get(url)
    data = res.json()
    return data['data'][0]['cid']


def getData(text):
    result = []  # 用于存储解析结果
    data = re.findall('<d p="(.*?)">(.*?)</d>', text)
    #<d p="40.44000,1,25,16777215,1665576457,0,6e5dee1b,1161698542704939520,11">痛，太痛了</d>
    for d in data:
        item = {}  # 每条弹幕数据
        dm = d[0].split(',')
        item['评论时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(dm[4])))
        item['用户ID'] = dm[6]
        item['弹幕内容'] = d[1]
        result.append(item)
    return result


def get_dm(bvid):
    cid = get_cid(bvid)
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=%d' % cid
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": "buvid3=8ECE4E42-6590-1C71-FB93-4908621889F129704infoc; _uuid=7210F71CF-8A7A-2AA8-10D29-FF6410996C6E929844infoc; i-wanna-go-back=-1; LIVE_BUVID=AUTO1116423810769769; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(u~)l~RJkYl0J'uYRkJ)uJ|R; buvid4=D0411CAE-FB69-458E-E835-9CDCCAD774EA87241-022012117-pi29DxjWV7fGnnEJST2ttA==; buvid_fp_plain=undefined; buvid_fp=c54eb9f524c20d4742e025536f04212e; DedeUserID=393276724; DedeUserID__ckMd5=f17390edbe173715; b_ut=5; nostalgia_conf=-1; hit-dyn-v2=1; b_nut=100; CURRENT_QUALITY=80; bsource=search_baidu; is-2022-channel=1; fingerprint3=1366fde42b1b72f7c5fba92b2cc38443; fingerprint=ab2541810f75a09d876559378b636dc2; b_lsid=8D73ED103_183CB6345B8; SESSDATA=4a8be6a6,1681119117,0e47d*a1; bili_jct=48cfbcf22e6ef3b1f566ec1064b231e0; bp_video_offset_393276724=716088734818238500; sid=6m926epl; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; PVID=1; innersign=1; CURRENT_FNVAL=4048",
    }
    res = requests.get(url=url,headers=headers)
    res.encoding = 'utf-8'
    text = res.text
    dms = getData(text)
    return dms


def main():
    dms = get_dm(bid)
    dms = pd.DataFrame(dms)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("删除成功")
    dms.to_csv(file_path, index=False)


if __name__ == '__main__':
    main()
