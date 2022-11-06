import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

player_csv = '../spider/lol/player-ranks.csv'
save_path = "../draw/"


def parse_csv(csv_path):
    pd_csv = pd.read_csv(csv_path)
    return pd_csv


def get_player_rank_by_meta(players):
    rank = []
    csv = parse_csv(player_csv)
    player_name = csv.get("playername").values
    teams = csv.get("teamname").values
    metas = csv.get("meta").values
    kda = csv.get("kda").values
    current_metas = [metas[i] for i in range(0, len(metas)) if player_name[i] in players]
    current_kda = [kda[i] for i in range(0, len(metas)) if player_name[i] in players]
    teams = [teams[i] for i in range(0, len(metas)) if player_name[i] in players]
    for j in range(0, len(current_metas)):
        all_meta_kda = [kda[i] for i in range(0, len(kda)) if current_metas[j] == metas[i]]
        all_meta_kda.sort(reverse=True)
        for i in range(0, len(all_meta_kda)):
            if current_kda[j] == all_meta_kda[i]:
                rank.append(i + 1)
                break
    return teams, rank


players = [["JackeyLove", "Hope", "GALA", "Viper"],
           ["knight", "Yagao", "Xiaohu", "Scout"],
           ["Wayward", "369", "Breathe", "Flandre"],
           ["Tian", "Kanavi", "Wei", "Jiejie"]]

teams = ["TES", "RNG", "JDG", "EDG"]
ranks = np.random.random((4, 4))

for j in range(0, len(players)):
    result = get_player_rank_by_meta(players[j])
    for i in range(0, len(result[1])):
        ranks[j][teams.index(result[0][i])] = result[1][i]

print(ranks)

df = pd.DataFrame(ranks, columns=teams, index=["ADC", "mid", "top", "jungle"])

pl = sns.heatmap(df, annot=True)
plt.savefig("../draw/hot.png")
plt.show()
