# -*- coding: utf-8 -*-
# @Time    : 17-12-17
# @Author  : Wutao Lin
# @Environment : Python 3.5
# @function:

import matplotlib.pyplot as plt


class LegendStyler():
    def __init__(self, loc='upper right', frameon=False, font_size=None, handlelength=None):
        """

        Args:
            loc:
            frameon:
            font_size:
            handlelength: 控制legend里面线的长度
        """
        self.loc = loc
        self.frameon = frameon
        self.prop = {
            'family': 'Times New Roman',
            'size': font_size,
        }
        self.handlelength = handlelength

    def get_loc(self):
        return self.loc

    def get_frameon(self):
        return self.frameon

    def get_prop(self):
        return self.prop

    def get_handlelength(self):
        return self.handlelength
