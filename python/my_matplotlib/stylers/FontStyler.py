# -*- coding: utf-8 -*-
# @Time    : 17-12-17
# @Author  : Wutao Lin
# @Environment : Python 3.5
# @function:

import matplotlib.pyplot as plt


class FontStyler():
    def __init__(self, font_family='Times New Roman', font_size=10):
        self.font_family = font_family
        self.font_size = font_size

    def set_global_font_family(self):
        plt.rc('font', family=self.font_family)



