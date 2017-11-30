# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def make_line_graph(x_ticks, y1, figure_path="test.jpg", figure_title="test", y1_desc="y1", y2_desc="y2", y2=None):
    """

    Args:
        x_ticks:  x轴标签
        y1:  第一个预测值的列
        figure_path: *.jpg
        figure_title:
        y1_desc: 图例描述
        y2_desc:
        y2:  第二个预测值的列

    Returns:

    """

    assert len(x_ticks) == len(y1)
    x = np.arange(len(x_ticks))

    y_max = y1.max()
    y_min = y1.min()

    if y2 is not None:
        assert len(y1) == len(y2)
        if y2.max() > y_max:
            y_max = y2.max()
        if y2.min() < y_min:
            y_min = y2.min()


    plt.figure(figsize=[7, 4])
    plt.ylim(y_min, y_max)

    plt.plot(x, y1, 'd-', label=y1_desc, linewidth=1.5, markersize=5, color="#0040FF")
    if y2 is not None:
        plt.plot(x, y2, '.-', label=y2_desc, linewidth=1.5, markersize=5, color="#FF0000")
        plt.legend(loc='upper right', frameon=False)

    else:
        plt.legend(loc='upper right', frameon=False)

    #plt.xlim(0.5, 6.5)
    #plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], [u'0%', u'10%', u'20%', u'30%', u'40%', u'50%'])

    plt.title(figure_title)
    plt.xlabel("Date")
    plt.xticks(x, x_ticks)
    plt.ylabel("Lend or Rent Number")
    plt.tight_layout()

    #plt.show()
    plt.savefig(figure_path)


if __name__ == "__main__":
    x_ticks = ["20151101", "20151102", "20151103", "20151104", "20151105", "20151106"]

    y1 = [0.778128, 0.733309, 0.684417, 0.432836, 0.666667, 0.522936]
    y2 = []
    for y in y1:
        y2.append(y - 0.2)

    make_line_graph(x_ticks, np.array(y1), y2=np.array(y2))
