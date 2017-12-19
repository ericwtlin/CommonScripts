# -*- coding: utf-8 -*-
# @Time    : 17-12-17
# @Author  : Wutao Lin
# @Environment : Python 3.5
# @function:

import matplotlib.pyplot as plt


class LineStyler(object):
    marker_size = 5
    line_width = 1.5
    def __init__(self, line_width=None, marker_size=None, select_styles=[], diff_line_style=False):
        """

        :param line_width:
        :param marker_size:
        :param select_styles:  a list contains the indices of self.line_styles
        :param diff_line_style: if False, all the line styles are the same
                                if True: the line will be different (solid line, dotted line, )
        """
        self.diff_line_style = diff_line_style
        self.update_style()

        if len(select_styles) != 0:
            self.line_styles = [self.line_styles[i] for i in select_styles]

        if line_width is not None:
            self.set_line_width(line_width)
        if marker_size is not None:
            self.set_marker_size(marker_size)


    def update_style(self):
        if self.diff_line_style == False:
            self.line_styles = [
                {
                    'style': '^-',      #三角形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,  # 这个三角形看着偏小一点
                    'color': '#ff9999'  # 浅粉色
                },
                {
                    'style': 's-',    #正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#00BFFF'  # 浅蓝色
                },
                {
                    'style': '*-',    # 五角星
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 3,
                    'color': '#b3ffb3'  # 浅绿色
                },
                {
                    'style': 'D-',    #菱形放置的正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#ffa366'  # 橙色
                },
                {
                    'style': '+-',    # +
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,
                    'color': '#999999'  # 灰色
                },
            ]
        else:
            self.line_styles = [
                {
                    'style': '^-',      #三角形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,  # 这个三角形看着偏小一点
                    'color': '#ff9999'  # 浅粉色
                },
                {
                    'style': 's--',    #正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#00BFFF'  # 浅蓝色
                },
                {
                    'style': '*-.',    # 五角星
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 3,
                    'color': '#b3ffb3'  # 浅绿色
                },
                {
                    'style': 'D:',    #菱形放置的正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#ffa366'  # 橙色
                },
                {
                    'style': '+-',    # +
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,
                    'color': '#999999'  # 灰色
                },
            ]

    def get_style(self, index):
        if index >= len(self.line_styles):
            raise Exception("The pre-defined line style is not enough!")
        return self.line_styles[index]

    def set_line_width(self, line_width):
        if isinstance(line_width, list):
            for i in range(len(line_width)):
                if i < len(self.line_styles):
                    self.line_styles[i]['line_width'] = line_width[i]
        elif isinstance(line_width, float) or isinstance(line_width, int):
            self.line_width = line_width
            self.update_style()

    def set_marker_size(self, marker_size):
        if isinstance(marker_size, list):
            for i in range(len(marker_size)):
                if i < len(self.line_styles):
                    self.line_styles[i]['marker_size'] = marker_size[i]
        elif isinstance(marker_size, float) or isinstance(marker_size, int):
            self.marker_size = marker_size
            self.update_style()


class FontStyler():
    def __init__(self, font_family='Times New Roman', font_size=10):
        self.font_family = font_family
        self.font_size = font_size

    def set_global_font_family(self):
        plt.rc('font', family=self.font_family)


class LegendStyler():
    def __init__(self, loc='upper right', frameon=False, font_size=11):
        self.loc = loc
        self.frameon = frameon
        self.prop = {
            'family': 'Times New Roman',
            'size': font_size,
        }

    def get_loc(self):
        return self.loc

    def get_frameon(self):
        return self.frameon

    def get_prop(self):
        return self.prop
