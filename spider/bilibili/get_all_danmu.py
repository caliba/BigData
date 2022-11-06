import pandas
import time
import bilibili_danmu


bv_path = "../lol/bv.csv"
all_damu_path = "alldanmu.csv"


def main():
    result = []
    with open(bv_path, "r", encoding="utf-8") as bv_file:
        i = 0
        for line in bv_file:
            if i == 0:
                i += 1
                continue
            bid = line.split(",")[-1].replace("\n", "")
            result += bilibili_danmu.get_dm(bid)
            time.sleep(1)

    pandas.DataFrame(result).to_csv(all_damu_path)


if __name__ == '__main__':
    main()
