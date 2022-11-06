import requests
from bs4 import BeautifulSoup
import json
import pandas

json_path = "player-stat-json-"
csv_path = "player-ranks.csv"


def get_url():
    url = 'https://www.wanplus.cn/lol/playerstats'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": "buvid3=8ECE4E42-6590-1C71-FB93-4908621889F129704infoc; _uuid=7210F71CF-8A7A-2AA8-10D29-FF6410996C6E929844infoc; i-wanna-go-back=-1; LIVE_BUVID=AUTO1116423810769769; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(u~)l~RJkYl0J'uYRkJ)uJ|R; buvid4=D0411CAE-FB69-458E-E835-9CDCCAD774EA87241-022012117-pi29DxjWV7fGnnEJST2ttA==; buvid_fp_plain=undefined; buvid_fp=c54eb9f524c20d4742e025536f04212e; DedeUserID=393276724; DedeUserID__ckMd5=f17390edbe173715; b_ut=5; nostalgia_conf=-1; hit-dyn-v2=1; b_nut=100; CURRENT_QUALITY=80; bsource=search_baidu; is-2022-channel=1; fingerprint3=1366fde42b1b72f7c5fba92b2cc38443; fingerprint=ab2541810f75a09d876559378b636dc2; b_lsid=8D73ED103_183CB6345B8; SESSDATA=4a8be6a6,1681119117,0e47d*a1; bili_jct=48cfbcf22e6ef3b1f566ec1064b231e0; bp_video_offset_393276724=716088734818238500; sid=6m926epl; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; PVID=1; innersign=1; CURRENT_FNVAL=4048",
    }
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")


def parse_json() -> list:
    player_list = []
    for i in range(1, 7):
        with open(json_path + str(i), "r") as json_file:
            decoder = json.JSONDecoder()
            player_list += decoder.decode(json_file.read())['data']
    return player_list


def main():
    pandas.DataFrame(parse_json()).to_csv(csv_path)


if __name__ == '__main__':
    main()


