import os
import pandas as pd
import requests
import time
import random

bv_path = "../lol/bv.csv"
max_page = 50
file_name = 'allc.csv'


def geturl(pn, oid):
    url = f"https://api.bilibili.com/x/v2/reply?pn={pn}&type=1&oid={oid}&sort=2"
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    text = r.json()['data']['replies']
    return text


def getData(aid):
    comment_list = []
    user_name = []
    for page in range(1, max_page+1):
        text = geturl(page, aid)
        for t in text:
            comment_list.append(t['content']['message'].replace("\n", "|"))
            user_name.append(t['member']['uname'])
    return user_name, comment_list


def main():
    result_user = []
    result_comment = []
    with open(bv_path, "r", encoding="utf-8") as bv_file:
        i = 0
        for line in bv_file:
            if i == 0:
                i += 1
                continue
            i += 1
            aid = line.split(",")[-2].replace("\n", "")
            u, c = getData(aid)
            result_user += u
            result_comment += c
            print(f"----------{len(result_user)}---------\n")
            print(f"----------{i}---------\n")
            time.sleep(random.randint(20, 30))  # 不sleep的话ip会被ban掉

    df = pd.DataFrame({
        '用户': result_user,
        '评论内容': result_comment
    })
    df.to_csv(file_name)


if __name__ == '__main__':
    main()
