import matplotlib.pyplot as plt
import pandas as pd
from math import pi

player_csv = '../spider/lol/player-ranks.csv'
save_path = "../draw/"


def parse_csv(csv_path):
    pd_csv = pd.read_csv(csv_path)
    return pd_csv


def get_players_data(players):
    csv = parse_csv(player_csv)
    player_name = csv.get("playername").values
    damageconvertrate = csv.get("damagetoheroConversionRate").values
    gold = csv.get("goldsPercent").values
    damage_taken = csv.get("damagetakenPercent").values
    damage_to = csv.get("damagetoheroPercent").values
    return pd.DataFrame({
        "group": [p for p in player_name if p in players],
        "damageconvertrate": [damageconvertrate[i] * 100 / 5 for i in range(0, len(damageconvertrate)) if player_name[i] in players],
        "goldPercent": [gold[i] * 100 for i in range(0, len(gold)) if player_name[i] in players],
        "damageTakenPercent": [float(damage_taken[i].replace("%", "")) for i in range(0, len(damage_taken)) if player_name[i] in players],
        "damageToHeroPercent": [float(damage_to[i].replace("%", "")) for i in range(0, len(damage_to)) if player_name[i] in players]
    })


players = ["JackeyLove", "Hope", "GALA", "Viper"]
df = get_players_data(players)
print(df)
categories = list(df)[1:]
N = len(categories)

angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

ax = plt.subplot(111, polar=True)
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

plt.xticks(angles[:-1], categories)
ax.set_rlabel_position(0)
# plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
# plt.ylim(0, 40)


for i in range(0, len(df.values)):
    values = df.loc[i].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle="solid", label=players[i])
    ax.fill(angles, values, alpha=0.1)


plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
plt.savefig("../draw/radar.png")
plt.show()

