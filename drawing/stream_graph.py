import jieba
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re


f = open('../spider/bilibili/alldanmu.csv', encoding='utf-8')
txt = f.read()
danmus = txt.split('\n')

wordCountByTime = {}


def count_word():
    for d in danmus[1:]:
        if d == "":
            continue
        time = d.split(",")[1].split(" ")[0]
        content = jieba.lcut(d.split(",")[-1])
        if time in wordCountByTime.keys():
            wordCount: dict = wordCountByTime[time]
            for word in content:
                if re.search(r"[a-zA-Z]+", word) is None:
                    continue
                word = word.strip().lower()
                if word in wordCount.keys():
                    wordCount[word] += 1
                else:
                    wordCount[word] = 1
        else:
            wordCount = {}
            for word in content:
                if re.search(r"[a-zA-Z]+", word) is None:
                    continue
                wordCount[word] = 1
            wordCountByTime[time] = wordCount


def remove_word():
    for k in wordCountByTime.keys():
        wc = wordCountByTime[k]
        key_to_remove = []
        for w in wc.keys():
            if wc[w] <= 5:
                key_to_remove.append(w)
        for w in key_to_remove:
            wc.pop(w)


def gaussian_smooth(x, y, grid, sd):
    weights = np.transpose([stats.norm.pdf(grid, m, sd) for m in x])
    weights = weights / weights.sum(0)
    return (weights * y).sum(1)


def find_words_count(words_to_find):
    result = []
    for i in range(0, len(words_to_find)):
        result.append([])
    for t in wordCountByTime.keys():
        wc: dict = wordCountByTime[t]
        counts = []
        need_add = False
        for wtf in words_to_find:
            if wtf in wc.keys():
                counts.append(wc[wtf])
                need_add = True
            else:
                counts.append(0)
        if need_add:
            for i in range(0, len(words_to_find)):
                result[i].append(counts[i])
    return result


words = ["tes", "jkl", "ts", "wbg"]
COLORS = ["red", "blue", "yellow", "orange"]
count_word()
remove_word()
y = find_words_count(words)
x = np.arange(0, len(y[0]))
fig, ax = plt.subplots(figsize=(10, 7))
grid = np.linspace(0, len(y[0]), num=500)
y_smoothed = [gaussian_smooth(x, y_, grid, 1) for y_ in y]
ax.stackplot(grid, y_smoothed, colors=COLORS, baseline="sym")
plt.legend(words)
plt.savefig("../draw/stream_graph.png")
plt.show()

