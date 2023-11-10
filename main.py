import os
import matplotlib.pyplot as plt
import pandas as pd
from inspect import getsourcefile
from os.path import abspath
import numpy as np
from matplotlib import patches
from matplotlib.ticker import ScalarFormatter
from pandas.plotting._matplotlib.style import get_standard_colors


def plot_multi(data, graph_names, cols=None, spacing=0.07, **kwargs):
    fig, ax = plt.subplots()

    cols = data.columns

    colors = get_standard_colors(num_colors=len(cols))

    plt.plot(data[cols[0]], data[cols[1]], color=colors[1], label="GRAPH_NAME")

    ax.set_ylabel(ylabel=graph_names[0], color=colors[1])

    lines = ax.get_lines()
    dia = len(cols) - 2
    for n in range(2, len(cols)):
        ax_new = ax.twinx()
        ax_new.spines["right"].set_position(("axes", 1 + spacing * (n - 2)))
        pd.Series(np.array(data[cols[n]]), index=data[cols[0]]).plot(
            color=colors[n], **kwargs, label=cols[n]
        )
        ax_new.set_ylabel(ylabel=graph_names[n - 1], color=colors[n])

        lines += ax_new.get_lines()

    fig.autofmt_xdate(rotation=35)
    ax.grid(True, color="grey", linewidth="0.5", axis='x')
    rr = 1.01 - dia * 0.053
    plt.subplots_adjust(left=0.06, top=1, right=rr)

    ax.legend(lines, [line.axes.get_ylabel() for line in lines])

    plt.show()


PROJECT_PATH = "/".join(abspath(getsourcefile(lambda: 0)).split("\\")[:-1])
FILES_PATH = "csv"

os.chdir(f"{PROJECT_PATH}/{FILES_PATH}")

graph_names = []
csvs = []
x_lable_list = []
for file in os.listdir():
    source_df = pd.read_csv(file, sep=";")
    GRAPH_NAME = source_df.columns[3][source_df.columns[3].rfind("«") + 1: source_df.columns[3].rfind("»")].capitalize()
    x_lable_list = list(source_df["Период"])
    y = list(int(i.replace(" ", "")) for i in source_df["Число запросов"])

    graph_names.append(GRAPH_NAME)

    csvs.append(y)
csvs.insert(0, x_lable_list)

keys = [i for i in range(len(csvs))]
values = [i for i in csvs]

dictionary = dict(zip(keys, values))

df = pd.DataFrame(dictionary)
plot_multi(df, graph_names=graph_names)
