# -*- coding: UTF-8 -*-
# This script is validated on Python 3.5

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, NullLocator
from scipy import interpolate

plt.rc('font',family='Times New Roman')

def make_sub_compare_graph(row_num, col_num, i, x1_data, y1_data, x2_data, y2_data, x3_data, y3_data, bar_width, title="", x_label="", y_label="", legend1="", legend2="", legend3="", x_range=[], y_range=[], xticks_x=[], xticks_label=[], yticks_y=[], yticks_label=[]):
	'''用于画对比子图
	x_range: 数组，x_range[0]表示最小值,x_range[1]表示最大值
	y_range: 数组，同x_range
	'''
	ax = plt.subplot(row_num, col_num, i)

	font = {'family': 'Times New Roman',
			}

	plt.title(title, fontdict=font)
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

	plt.bar(x1_data, y1_data, bar_width, label=legend1, hatch='//', color='white', edgecolor='#FE2E2E')
	plt.bar(x2_data, y2_data, bar_width, label=legend2, hatch='.', color='white', edgecolor='#00BFFF')
	plt.bar(x3_data, y3_data, bar_width, label=legend3, hatch='+', color='white', edgecolor='#A5DF00')

	font_legend = {'family': 'Times New Roman',
			'size': 10,
			}
	plt.legend(loc='upper right',frameon=False, prop=font_legend)

	#在第一个条形上面添加y值
	for x, y in zip(x1_data, y1_data):
		plt.text(x+bar_width/2, y+0.005, "%.4f" % y, ha='center', va='bottom', fontsize='9', fontdict=font)
	#在第二个条形上添加y值
	for x, y in zip(x2_data, y2_data):
		plt.text(x+bar_width/2, y+0.005, "%.4f" % y, ha='center', va='bottom', fontsize='9', fontdict=font)

	for x, y in zip(x3_data, y3_data):
		plt.text(x + bar_width / 2, y + 0.005, "%.4f" % y, ha='center', va='bottom', fontsize='9', fontdict=font)


def make_label_compare_graph(row_num, col_num):
	'''画对比结果,此函数用于总控
	'''
	fig = plt.figure(figsize = [8, 6])	#[width, height]
	bar_width = 0.7
	gap_bars_width = 0.3 	#同组的bar之间的间隔
	gap_groups_width = 0.8	#不同组之间的间隔
	start = 0.2
	x1_data = []; x2_data = []; x3_data = []; xticks_x = [];
	for i in range(0, 3):
		#print(i)
		x1_data.append(start + (3 * bar_width + gap_bars_width + gap_groups_width) * i)
		x2_data.append(x1_data[i] + bar_width + gap_bars_width)
		x3_data.append(x2_data[i] + bar_width + gap_bars_width)
		#xticks_x.append(x1_data[i] + bar_width + gap_bars_width / 2 )
		xticks_x.append(x2_data[i] + bar_width / 2)

	xticks_label = ['Precision', 'Recall', 'F$_1$-Score']
	legend1 = "M1"
	legend2 = "M2"
	legend3 = "M3"

	contiguous_improved = [0.82, 0.70, 0.76]
	discontiguous_improved = [0.70, 0.31, 0.43]
	overlapping_improved = [0.86, 0.28, 0.42]
	total_improved = [0.82, 0.66, 0.73]

	contiguous_biohd = [0.69, 0.63, 0.60]
	discontiguous_biohd = [0.57, 0.28, 0.31]
	overlapping_biohd = [0.37, 0.17, 0.24]
	total_biohd = [0.68, 0.60, 0.64]

	contiguous_biohd1234 = [0.69, 0.64, 0.66]
	discontiguous_biohd1234 = [0.57, 0.27, 0.37]
	overlapping_biohd1234 = [0.38, 0.22, 0.28]
	total_biohd1234 = [0.68, 0.61, 0.64]


	#画第一个subplot：contiguous
	title = "Contiguous mention"
	x_label = ""
	y_label = ""
	x_range = [0, x3_data[2] + bar_width + start]
	y_range = [0.6, 1.0]
	yticks_y = [0.6, 0.7, 0.8, 0.9, 1.0]
	yticks_label = [u'0.6', u'0.7', u'0.8', u'0.9', u'1.0']

	make_sub_compare_graph(row_num, col_num, 1, x1_data, contiguous_improved, x2_data, contiguous_biohd,
			x3_data, contiguous_biohd1234, bar_width, title, x_label, y_label, legend1, legend2, legend3,
			x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)


	#画第二个subplot：discontiguous
	title = "Discontiguous mention"
	x_label = ""
	y_label = ""
	y_range = [0.2, 1.0]
	yticks_y = [0.2, 0.4, 0.6, 0.8, 1.0]
	yticks_label = [u'0.2', u'0.4', u'0.6', u'0.8', u'1.0']
	make_sub_compare_graph(row_num, col_num, 2, x1_data, discontiguous_improved, x2_data, discontiguous_biohd, x3_data,
		   discontiguous_biohd1234, bar_width, title, x_label, y_label, legend1, legend2, legend3, x_range,
		   y_range, xticks_x, xticks_label, yticks_y, yticks_label)

	#画第三个subplot：overlapping
	title = "Overlapping mention"
	x_label = ""
	y_label = ""
	y_range = [0.0, 1.0]
	yticks_y = []
	yticks_label = []
	make_sub_compare_graph(row_num, col_num, 3, x1_data, overlapping_improved, x2_data, overlapping_biohd, x3_data,
						   overlapping_biohd1234, bar_width, title, x_label, y_label, legend1, legend2, legend3,
						   x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)

	#画第四幅图subplot: total
	title = "All mentions"
	x_label = ""
	y_label = ""
	y_range = [0.5, 1.0]
	yticks_y = []
	yticks_label = []
	make_sub_compare_graph(row_num, col_num, 4, x1_data, total_improved, x2_data, total_biohd, x3_data,
						   total_biohd1234, bar_width, title, x_label, y_label, legend1, legend2, legend3,
						   x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)

	plt.tight_layout()
	#plt.show()
	plt.savefig('bar_compare_multiple_2x2.png', dpi=300)


def make_model_compare_graph(row_num, col_num):
	'''figure 6, 画M1与M2模型的对比，此模型作为总控
	'''
	fig = plt.figure(figsize = [10, 3])	#[width, height]

	bar_width = 3
	gap_bars_width = 1.3 	#同组的bar之间的间隔
	gap_groups_width = 3	#不同组之间的间隔
	start = 1
	x1_data = []; x2_data = []; xticks_x = [];
	for i in range(0, 3):
		#print(i)
		x1_data.append(start + (2 * bar_width + gap_bars_width + gap_groups_width) * i)
		x2_data.append(x1_data[i] + bar_width + gap_bars_width)
		xticks_x.append(x1_data[i] + bar_width + gap_bars_width / 2 )

	xticks_label = ['Precision', 'Recall', 'F$_1$-Score']

	svm_strict = [0.82, 0.66, 0.73]
	svm_left_match = [0.82, 0.68, 0.74]
	svm_right_match = [0.84, 0.69, 0.76]
	M2_strict = [0.81, 0.64, 0.71]
	M2_left_match = [0.82, 0.66, 0.73]
	M2_right_match = [0.84, 0.67, 0.75]

	#画第一幅图strict
	title = "Strict Mode"
	x_label = ""
	y_label = ""
	x_range = [0, x2_data[2] + bar_width + start]
	y_range = [0.5, 0.9]
	yticks_y = []
	yticks_label = []
	legend2 = "M1"
	legend1 = "M2"
	#make_sub_compare_graph(row_num, col_num, 1, x1_data, svm_strict, x2_data, M2_strict, bar_width, title, x_label, y_label, legend1, legend2, x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)
	make_sub_compare_graph(row_num, col_num, 1, x1_data, M2_strict, x2_data, svm_strict, bar_width, title, x_label, y_label, legend1, legend2, x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)

	#画第二幅图left match
	title = "Left Match Mode"
	x_label = ""
	y_label = ""
	x_range = [0, x2_data[2] + bar_width + start]
	y_range = [0.5, 0.9]
	yticks_y = []
	yticks_label = []
	legend2 = "M1"
	legend1 = "M2"
	make_sub_compare_graph(row_num, col_num, 2, x1_data, M2_left_match, x2_data, svm_left_match, bar_width, title, x_label, y_label, legend1, legend2, x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)


	#画第三幅图left match
	title = "Right Match Mode"
	x_label = ""
	y_label = ""
	x_range = [0, x2_data[2] + bar_width + start]
	y_range = [0.5, 0.9]
	yticks_y = []
	yticks_label = []
	legend2 = "M1"
	legend1 = "M2"
	make_sub_compare_graph(row_num, col_num, 3, x1_data, M2_right_match, x2_data, svm_right_match, bar_width, title, x_label, y_label, legend1, legend2, x_range, y_range, xticks_x, xticks_label, yticks_y, yticks_label)

	plt.tight_layout()
	#plt.show()
	plt.savefig('bar_compare_multiple_1x3.png', dpi=300)




def main():
	make_distance_graph()

	make_label_compare_graph(2, 2)

	make_model_compare_graph(1, 3)



if __name__ == "__main__":
	main()


