import matplotlib.pyplot as plt
import pandas as pd

team_csv = '../spider/lol/team-ranks.csv'
player_csv = '../spider/lol/player-ranks.csv'
save_path = "../draw/"


def parse_csv(csv_path):
    pd_csv = pd.read_csv(csv_path)
    return pd_csv


def team_plot_draw():
    csv = parse_csv(team_csv)
    teams: pd.Series = csv.get("teamname").values
    kda = csv.get("kda").values
    gold = csv.get("goldsPermin").values
    fig = plt.figure(figsize=(8, 4), dpi=100)
    ax1 = fig.add_subplot(111)
    line1, = ax1.plot(teams, kda, 'b:', label="kda")
    ax2 = ax1.twinx()
    line2, = ax2.plot(teams, gold, 'g-', label="gold per match")
    plt.legend((line1, line2), ('kda', "gold per min"))
    ax1.set_ylabel("kda")
    ax2.set_ylabel("gold per min")
    ax1.set_xlabel("team")
    plt.savefig(f"{save_path}/team_plot.png")
    plt.show()


def player_plot_draw():
    csv = parse_csv(player_csv)
    player: pd.Series = csv.get("playername").values
    meta = csv.get("meta").values
    teams = csv.get("teamname").values
    kda = csv.get("kda").values
    gold = csv.get("goldsPercent").values
    damage_taken = csv.get("damagetakenPercent").values
    damage_to = csv.get("damagetoheroPercent").values
    for m in ["中单", "ADC", "上单", "打野"]:
        fig = plt.figure(figsize=(40, 20), dpi=100)
        ax1 = fig.add_subplot(111)
        line1, = ax1.plot([player[i] + "/" + teams[i] for i in range(0, len(player)) if meta[i] == m], [kda[i] for i in range(0, len(player)) if meta[i] == m], 'b:', label="kda")
        ax2 = ax1.twinx()
        line2, = ax2.plot([player[i] + "/" + teams[i] for i in range(0, len(player)) if meta[i] == m], [float(gold[i] * 100) for i in range(0, len(player)) if meta[i] == m], 'g-', label="goldsPercent")
        line3, = ax2.plot([player[i] + "/" + teams[i] for i in range(0, len(player)) if meta[i] == m], [float(damage_to[i].replace("%", "")) for i in range(0, len(player)) if meta[i] == m], 'r-', label="damageToHeroPercent")
        line4, = ax2.plot([player[i] + "/" + teams[i] for i in range(0, len(player)) if meta[i] == m], [float(damage_taken[i].replace("%", "")) for i in range(0, len(player)) if meta[i] == m], 'y-', label="damageTakenPercent")
        plt.legend((line1, line2, line3, line4), ('kda', "goldsPercent", "damageToHeroPercent", "damageTakenPercent"))
        ax1.set_ylabel("kda")
        ax2.set_ylabel("percent")
        ax1.set_xlabel("player name")
        plt.savefig(f"{save_path}/player_plot_{m}.png")
        plt.show()


def main():
    # team_plot_draw()
    player_plot_draw()


if __name__ == '__main__':
    main()
