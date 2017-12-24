# -*- coding: utf-8 -*-
# @Time    : 17-12-17
# @Author  : Wutao Lin
# @Environment : Python 3.5
# @function:

import matplotlib.pyplot as plt


class LineStyler(object):
    marker_size = 5
    line_width = 1.5


    def __init__(self, line_width=None, marker_size=None, select_styles=[], style_solution_idx=1):
        """

        Args:
            line_width:
            marker_size:
            select_styles:  a list contains the indices of self.line_styles
            style_solution:
            specific_style_templates:
        """


        self.style_solution_idx = style_solution_idx
        self.update_style()

        if len(select_styles) != 0:
            self.line_styles = [self.line_styles[i] for i in select_styles]

        if line_width is not None:
            self.set_line_width(line_width)
        if marker_size is not None:
            self.set_marker_size(marker_size)


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


    def update_style(self):
        """
        目前有2个solution，
            第一个solution是线都是实线，但是有不同图标、不同颜色
            第二个solution是有4条线，头两个是一组：一个实线一个虚线，后两个是一组，一个实线一个虚线；两组的图标不一样
        Returns:

        """
        self.style_solutions = [
            [
                {
                    'style': '^-',  # 三角形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,  # 这个三角形看着偏小一点
                    'color': '#ff9999'  # 浅粉色
                },
                {
                    'style': 's-',  # 正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#00BFFF'  # 浅蓝色
                },
                {
                    'style': '*-',  # 五角星
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 3,
                    'color': '#b3ffb3'  # 浅绿色
                },
                {
                    'style': 'D-',  # 菱形放置的正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#ffa366'  # 橙色
                },
                {
                    'style': '+-',  # +
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,
                    'color': '#999999'  # 灰色
                },
            ],
            [
                {
                    'style': '^-',  # 三角形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 1.5,  # 这个三角形看着偏小一点
                    'color': '#ff9999'  # 浅粉色
                },
                {
                    'style': 's--',  # 正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#ff9999'  # 浅蓝色
                },
                {
                    'style': '*-',  # 五角星
                    'line_width': self.line_width,
                    'marker_size': self.marker_size + 3,
                    'color': '#00BFFF'  # 浅绿色
                },
                {
                    'style': 'D--',  # 菱形放置的正方形
                    'line_width': self.line_width,
                    'marker_size': self.marker_size,
                    'color': '#00BFFF'  # 橙色
                },

            ]
        ]

        self.line_styles = self.style_solutions[self.style_solution_idx]



