# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def write_excel():
    analysis_path = "test.xlsx"
    df = pd.DataFrame({
        u'类别': [''] * 100,
        u'备注': [''] * 100,
        u'没预测出来': np.arange(100),
        u'预测错': np.arange(100),
        u'句子': np.arange(100),
        u'答案': np.arange(100)
    })
    df = df.ix[:, [u'类别', u'备注', u'预测错', u'没预测出来', u'句子', u'答案']]  # 按指定列顺序排序
    excel_writer = pd.ExcelWriter(analysis_path)
    df.to_excel(excel_writer, 'Not Pred')


if __name__ == "__main__":
    write_excel()