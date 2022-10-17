#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 2:19 PM
# @Author  : Agonsle
# @Site    : 爬取评论 有限制暂不明原因
# @File    : comments_weibo.py
# @Software: PyCharm
import os
import re

import requests
import pandas as pd
from time import sleep
import random
from fake_useragent import UserAgent

comments_file = 'contents.csv'


def main():
    weibo_list = ['4823279339309055', ]
    max_page = 10
    # comments_file = 'contents.csv'
    for weibo_id in weibo_list:
        max_id = '0'
        for page in range(1, max_page + 1):
            wait_second = random.uniform(0, 1)
            sleep(wait_second)
            if page == 1:
                url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(weibo_id, weibo_id)
            else:
                if max_id == '0':
                    break
                url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&max_id={}'.format(weibo_id,
                                                                                                            weibo_id,
                                                                                                            max_id)

            ua = UserAgent(verify_ssl=False)
            headers = {
                "User-Agent": ua.random,
                # 'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "cookie":"WEIBOCN_FROM=1110006030; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; __bid_n=183c26aced455b3a004207; FPTOKEN=30$RMDzNk06J0gA3a+ZyYR7qXFgu2P0CikMTuUtkvRUjaioK7GZ0EL7ueB2XhQmEyTyoVJDiTESgj5d2mANr2CJxdMN5nKDyGyivCcsDenYwOz2MCHht3ZLZmvekdkyK40Kr05fFR3A8F0ImXE1XHgVqHuuMYnnibj59sfPWeGsPCm5oxrnwQiFr/lSdwB62CTGbifrPJRe70XKEBW9X9pBW3mowloisir9mxy5orsfuykkItFtqwon2foMsZI6PrKFrKU42hfQCmNvcxgQUFuWAGXIyAgZb3ljz7+pDjK+3HewNofcZAXNTVyumiKkyBI+zUy6Rqp+iB9m32kEBIPtxsK0MJo6CAud++XJ9Jw59ZbTreKDWLa4lHmq2O6t55rb|BW2+EzBXU08V7qAO7DL0N+83QmwSltf/Cbr7G5Xj1j4=|10|120fdb16ffc418b529a4d4acfc9cf47b; SUB=_2A25OQEj4DeRhGeBI7lUR8ijKzz6IHXVty2iwrDV6PUJbkdAKLU_akW1NRpRJWm6BRn2KPAuWph3bxHvf3KUaY6Hm; _T_WM=44673473784; BAIDU_SSP_lcr=https://security.weibo.com/; MLOGIN=1; XSRF-TOKEN=28484e; mweibo_short_token=69811531a4; M_WEIBOCN_PARAMS=oid=4823279339309055&luicode=20000061&lfid=4823279339309055",
                # "cookie":"WEIBOCN_FROM=1110006030; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; __bid_n=183c26aced455b3a004207; FPTOKEN=30$RMDzNk06J0gA3a+ZyYR7qXFgu2P0CikMTuUtkvRUjaioK7GZ0EL7ueB2XhQmEyTyoVJDiTESgj5d2mANr2CJxdMN5nKDyGyivCcsDenYwOz2MCHht3ZLZmvekdkyK40Kr05fFR3A8F0ImXE1XHgVqHuuMYnnibj59sfPWeGsPCm5oxrnwQiFr/lSdwB62CTGbifrPJRe70XKEBW9X9pBW3mowloisir9mxy5orsfuykkItFtqwon2foMsZI6PrKFrKU42hfQCmNvcxgQUFuWAGXIyAgZb3ljz7+pDjK+3HewNofcZAXNTVyumiKkyBI+zUy6Rqp+iB9m32kEBIPtxsK0MJo6CAud++XJ9Jw59ZbTreKDWLa4lHmq2O6t55rb|BW2+EzBXU08V7qAO7DL0N+83QmwSltf/Cbr7G5Xj1j4=|10|120fdb16ffc418b529a4d4acfc9cf47b; SUB=_2A25OQEj4DeRhGeBI7lUR8ijKzz6IHXVty2iwrDV6PUJbkdAKLU_akW1NRpRJWm6BRn2KPAuWph3bxHvf3KUaY6Hm; _T_WM=44673473784; BAIDU_SSP_lcr=https://security.weibo.com/; MLOGIN=1; XSRF-TOKEN=d14d4a; M_WEIBOCN_PARAMS=oid=4822988379133474&luicode=20000061&lfid=4822988379133474&uicode=20000061&fid=4822988379133474; mweibo_short_token=82741c26f1",
                # "cookie":"WEIBOCN_FROM=1110006030; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; __bid_n=183c26aced455b3a004207; FPTOKEN=30$RMDzNk06J0gA3a+ZyYR7qXFgu2P0CikMTuUtkvRUjaioK7GZ0EL7ueB2XhQmEyTyoVJDiTESgj5d2mANr2CJxdMN5nKDyGyivCcsDenYwOz2MCHht3ZLZmvekdkyK40Kr05fFR3A8F0ImXE1XHgVqHuuMYnnibj59sfPWeGsPCm5oxrnwQiFr/lSdwB62CTGbifrPJRe70XKEBW9X9pBW3mowloisir9mxy5orsfuykkItFtqwon2foMsZI6PrKFrKU42hfQCmNvcxgQUFuWAGXIyAgZb3ljz7+pDjK+3HewNofcZAXNTVyumiKkyBI+zUy6Rqp+iB9m32kEBIPtxsK0MJo6CAud++XJ9Jw59ZbTreKDWLa4lHmq2O6t55rb|BW2+EzBXU08V7qAO7DL0N+83QmwSltf/Cbr7G5Xj1j4=|10|120fdb16ffc418b529a4d4acfc9cf47b; SUB=_2A25OQEj4DeRhGeBI7lUR8ijKzz6IHXVty2iwrDV6PUJbkdAKLU_akW1NRpRJWm6BRn2KPAuWph3bxHvf3KUaY6Hm; _T_WM=44673473784; BAIDU_SSP_lcr=https://security.weibo.com/; MLOGIN=1; XSRF-TOKEN=79cd04; mweibo_short_token=5e7ecafa7b; M_WEIBOCN_PARAMS=oid=4823153764729438&luicode=10000011&lfid=102803&uicode=20000061&fid=4823153764729438",
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br",
                "refer": "https://m.weibo.cn/detail/{}".format(weibo_id),
                "x-requested-with": "XMLHttpRequest",
                "mweibo-pwa": '1',
                "MWeibo-Pwa":"1",
                "X-XSRF-TOKEN":"c6d8ba"
            }
            r = requests.get(url, headers=headers)
            # print(r.status_code)
            # print(r.json())
            try:
                max_id = r.json()['data']['max_id']
                print(str(max_id))
                # print(r.json()['data']['max_id'])
                datas = r.json()['data']['data']
            except Exception as e:
                print("error")
                continue
            user_name = []
            text_list = []
            for data in datas:
                dr = re.compile(r'<[^>]+>', re.S)
                text2 = dr.sub('', data['text'])
                user_name.append(data['user']['screen_name'])
                text_list.append(text2)
            df = pd.DataFrame({
                '用户': user_name,
                '评论内容': text_list
            })
            if os.path.exists(comments_file):
                header = False
            else:
                header = True
            df.to_csv(comments_file, mode='a+', index=False, header=header, encoding='utf_8_sig')

    # print(text_list)
    # print(user_name)


if __name__ == "__main__":
    if os.path.exists(comments_file):
        os.remove(comments_file)
        print("删除完成")
    main()
