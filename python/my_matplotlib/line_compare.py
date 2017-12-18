# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from . import LineStyler, LegendStyler

plt.rc('font',family='Times New Roman')

def make_line_graph(x_list, y_lists, x_label, y_label, legends, x_ticks=None, figure_path=None, figure_title=None, figure_size=[5, 3],
        line_styler=None, legend_styler=None, y_range=None):
    assert len(y_lists) == len(legends)
    assert len(x_list) == len(y_lists[0]) == len(x_ticks)

    if y_range is None:
        y_max = - float('inf')
        y_min = float('inf')

        for y_list in y_lists:
            for y in y_list:
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
        y_max = y_max * 1.05
        y_min = y_min * 0.95
    else:
        y_min = y_range[0]
        y_max = y_range[1]

    if line_styler is None:
        line_styler = LineStyler()
    if legend_styler is None:
        legend_styler = LegendStyler()


    plt.figure(figsize=figure_size)
    plt.ylim(y_min, y_max)

    if x_ticks is not None:
        plt.xticks(x_list, x_ticks)

    for i in range(len(y_lists)):
        cur_style = line_styler.get_style(i)
        plt.plot(x_list, y_lists[i], cur_style['style'], label=legends[i], linewidth=cur_style['line_width'],
            markersize=cur_style['marker_size'], markeredgecolor=cur_style['color'], color=cur_style['color'])

    plt.legend(loc=legend_styler.loc, frameon=legend_styler.frameon, prop=legend_styler.prop)
    if figure_title is not None:
        plt.title(figure_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    if figure_path is None:
        plt.show()
    else:
        plt.savefig(figure_path, dpi=300)


if __name__ == "__main__":
    x_ticks = ["20151101", "20151102", "20151103", "20151104", "20151105", "20151106"]
    x_lists = np.arange(len(x_ticks))

    y1 = [0.778128, 0.733309, 0.684417, 0.432836, 0.666667, 0.522936]
    y2 = []
    for y in y1:
        y2.append(y - 0.2)
    y_lists = [y1, y2]
    make_line_graph(x_lists, y_lists, "test_x", "test_y", ['y1', 'y2'], x_ticks=x_ticks, figure_path='line_compare.png',
        figure_title=None, figure_size=[7, 4])

