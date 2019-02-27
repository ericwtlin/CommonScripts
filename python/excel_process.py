# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from openpyxl import load_workbook


def read_excel(excel_path):
    sheets = pd.read_excel(excel_path, sheetname=None)      #get all sheets
    print(sheets['sheet1'])

    sheet = pd.read_excel(excel_path, sheetname="sheet1")   #get specific sheet

    print(sheet['col_name'])

    row_num = 5
    print(sheet.get_value(row_num, 'col_name'))

def write_excel():
    analysis_path = "test.xlsx"
    df = pd.DataFrame({
        '类别': [''] * 100,
        '备注': [''] * 100,
        '没预测出来': np.arange(100),
        '预测错': np.arange(100),
        '句子': np.arange(100),
        '答案': np.arange(100)
    })

    row_num = col_num = 5
    df.set_value(row_num, col_num, "content to write")

    df = df.ix[:, ['类别', '备注', '预测错', '没预测出来', '句子', '答案']]  # 按指定列顺序排序


    excel_writer = pd.ExcelWriter(analysis_path, engine='xlsxwriter')
    df.to_excel(excel_writer, 'Not Pred')
    excel_writer.save()
    excel_writer.close()

    df2 = pd.DataFrame({'类别2': [''] * 100, '备注2': [''] * 100, '没预测出来2': np.arange(100), '预测错2': np.arange(100), '句子2': np.arange(100), '答案2': np.arange(100)})
    book = load_workbook(analysis_path)
    excel_writer = pd.ExcelWriter(analysis_path, engine='openpyxl')
    excel_writer.book = book
    df2.to_excel(excel_writer, sheet_name='Not Pred2')
    excel_writer.save()    # necessary
    excel_writer.close()



if __name__ == "__main__":
    write_excel()