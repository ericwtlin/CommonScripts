# -*- coding: UTF-8 -*-
# This script is used for making bar comparison graph.
# Environment: Both python 2.7 and python 3.5 are OK.

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, NullLocator
from scipy import interpolate

def make_model_compare_graph():
    fig = plt.figure(figsize = [5.5, 3])    #[width, height]

    bar_width = 2.5
    gap_bars_width = 1     #同组的bar之间的间隔
    gap_groups_width = 3    #不同组之间的间隔
    start = 1
    x1_data = []; x2_data = []; xticks_x = [];
    for i in range(0, 3):
        #print(i)
        x1_data.append(start + (2 * bar_width + gap_bars_width + gap_groups_width) * i)
        x2_data.append(x1_data[i] + bar_width + gap_bars_width)
        xticks_x.append(x1_data[i] + bar_width + gap_bars_width / 2)
        print(x1_data[i] + bar_width + gap_bars_width / 2)

    xticks_label = ['SL=0.01', 'SL=0.02', 'SL=0.03']

    exp1_result = [0, 56.09, 12.82]
    exp2_result = [58.66, 17.98, 8.47]
    dbscan_time = [2.43] * len(exp2_result)

    #画第一幅图strict
    x_label = "Side Length"
    y_label = "Computation Time"
    x_range = [0, x2_data[2] + bar_width + start]
    y_range = [0, 70]
    yticks_y = []
    yticks_label = []
    legend1 = "Data1"
    legend2 = "Data2"
    legend3 = "Data3"

    font = {'family': 'Times New Roman', 'size': 12}

    #plt.title(title, fontdict=font)
    plt.xlabel(x_label,fontdict=font)
    plt.ylabel(y_label, fontdict=font)

    if len(x_range) != 0:
        plt.xlim(x_range[0], x_range[1])
    if len(y_range) != 0:
        plt.ylim(y_range[0], y_range[1])

    #plt.tick_params(length=0)
    plt.tick_params(bottom='off', top='off')

    if len(xticks_x) != 0 and len(xticks_label) == len(xticks_x):
        plt.xticks(xticks_x, xticks_label, family='Times New Roman')
    else:
        plt.xticks(family='Times New Roman')

    if len(yticks_y) != 0 and len(yticks_label) == len(yticks_y):
        plt.yticks(yticks_y, yticks_label, family='Times New Roman')
    else:
        plt.yticks(family='Times New Roman')

    plt.bar(x1_data, exp1_result, bar_width, label=legend1, hatch='//', color='white', edgecolor='#F7819F')
    plt.bar(x2_data, exp2_result, bar_width, bottom=dbscan_time, label=legend2, hatch='.', color='white', edgecolor='#00BFFF')
    plt.bar(x2_data, dbscan_time, bar_width, label=legend3, hatch='.', color='white', edgecolor='#81F781')

    font_legend = {'family': 'Times New Roman',
            'size': 11,
            }
    plt.legend(loc='upper right',frameon=False, prop=font_legend)

    #在第一个条形上面添加y值
    for x, y in zip(x1_data, exp1_result):
        if y == 0:
            plt.text(x+bar_width/2, y+15, "Not appliable", rotation='vertical', ha='center', va='bottom', fontsize='11', fontdict={'family': 'Times New Roman', 'size': 12, 'color': '#F7819F'})
        else:
            plt.text(x+bar_width/2, y+0.005, "%.2f" % y, ha='center', va='bottom', fontsize='11', fontdict=font)
    #在第二个条形上添加y值
    for x, y, bottom in zip(x2_data, exp2_result, dbscan_time):
        plt.text(x+bar_width/2, bottom + y+0.005, "%.2f" % y, ha='center', va='bottom', fontsize='11', fontdict=font)

    plt.tight_layout()
    #plt.show()
    plt.savefig('bar_stacked_compare.png', dpi=300)



def main(report_path):
    make_model_compare_graph()

if __name__ == "__main__":
    report_path="dummy"
    main(report_path)


