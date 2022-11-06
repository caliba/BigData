import requests
from bs4 import BeautifulSoup
import json
import pandas
import time

mid = 50329118  # up主id
ps = 30  # 当页显示视频数
csv_path = "videos.csv"
bv_path = "bv.csv"


def get_url():
    # 获取up 视频合集第6页到16页的视频信息 (30个视频一页)
    video_list = []
    for page in range(6, 17):
        url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps={ps}&tid=0&pn={page}&keyword=&order=pubdate&order_avoided=true&jsonp=jsonp'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        cookies = {
            "_uuid": "472B110E10-66E1-C6A4-E8DD-7B82FCB26DB1070355infoc",
            "b_lsid": "9DCA816D_18446786EC5",
            "b_nut": "100",
            "b_ut": "5",
            "bili_jct": "cb37aaeca8cbee8b1af682511aab1e63",
            "blackside_state": "0",
            "bp_video_offset_325953543": "724916554764910600",
            "bsource": "search_baidu",
            "buvid_fp": "d306964fa516f770236604205d65a761",
            "buvid_fp_plain": "undefined",
            "buvid3": "2D45896A-1A49-2E85-5A0F-96DCDA1068BA70210infoc",
            "buvid4": "F82AE282-DF7B-368B-8041-D8F033CC42E170916-022061119-0wUJZf2fFJtdHar5eVUDeA==",
            "CURRENT_BLACKGAP": "0",
            "CURRENT_FNVAL": "4048",
            "CURRENT_QUALITY": "116",
            "DedeUserID": "325953543",
            "DedeUserID__ckMd5": "1a7bad4ba8e5efe9",
            "fingerprint": "18407c7147756c35ca0b684ce2a44aa9",
            "fingerprint3": "6f1737a52dc7120ee22b66264620c146",
            "go_old_video": "-1",
            "hit-dyn-v2": "1",
            "i-wanna-go-back": "-1",
            "innersign": "0",
            "is-2022-channel": "1",
            "LIVE_BUVID": "AUTO1716570249211752",
            "nostalgia_conf": "-1",
            "PVID": "1",
            "rpdid": "|(JJmYRR)Jlm0J'uYlRmRl~uR",
            "SESSDATA": "98d8e5b7,1683179716,f671c*b1",
            "sid": "eugphykd"
        }
        res = requests.get(url=url, headers=headers, cookies=cookies)
        res.encoding = 'utf-8'
        print(res.json())
        video_list += res.json()['data']['list']["vlist"]
        time.sleep(1)  # 别给我ip ban了
    return video_list


def parse_bv():
    csv = pandas.read_csv(csv_path)
    sub_csv = csv.get(["title", "aid", "bvid"])
    sub_csv[sub_csv["title"].str.contains("2022LPL夏季赛")].to_csv(bv_path)  # 过滤一下 只要今年夏季赛的视频


def main():
    # pandas.DataFrame(get_url()).to_csv(csv_path)
    parse_bv()


if __name__ == '__main__':
    main()
