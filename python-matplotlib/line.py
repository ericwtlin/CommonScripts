# -*- coding: UTF-8 -*-
# This script is

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, NullLocator
from scipy import interpolate

def make_distance_graph():
	'''画出不同span width情况下，mention的识别情况
	'''
	plt.figure(figsize=[7, 4])
	x = [1, 2, 3, 4, 5, 6]
	f_score = [0.778128, 0.733309, 0.684417, 0.432836, 0.666667, 0.522936]

	x_smooth = np.arange(1, 6, 0.15)
	tck_average = interpolate.splrep(x, f_score, s = 0.02)
	f_score_smooth = interpolate.splev(x_smooth, tck_average, der = 0)
	#plt.plot(x_smooth, f_score_smooth, linewidth=30, color="#E6E6E6")

	plt.plot(x, f_score, 'd-', linewidth=1.5, markersize=8, color="#0040FF")
	plt.xlim(0.5, 6.5)
	plt.ylim(0.3, 0.85)
	#plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], [u'0%', u'10%', u'20%', u'30%', u'40%', u'50%'])
	font = {'family': 'Times New Roman',
			}
	#plt.title("Results of mentions with Different Span Length", fontdict=font, fontsize=15)
	plt.xlabel("Span length", fontdict=font, fontsize=13)
	plt.xticks([1, 2, 3, 4, 5, 6], [u'0', u'1', u'2', u'3', u'4', u'5 or more' ], family='Times New Roman', fontsize=12)
	plt.yticks(family='Times New Roman', fontsize=12)
	plt.ylabel("", fontdict=font, fontsize=13)
	plt.tight_layout()
	#plt.show()
	plt.savefig('line.png', dpi=300)


def main():
	make_distance_graph()



if __name__ == "__main__":
	main()


