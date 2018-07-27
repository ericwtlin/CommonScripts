# -*- coding: utf-8 -*-


import logging
import argparse
import codecs
import matplotlib.pyplot as plt
import numpy as np
import nltk
from tqdm import tqdm

def hist_statistics(data_path, query_figure_path=None, passage_figure_path=None, sample_num=None):
    query_lengths = []
    passage_lengths = []
    with codecs.open(data_path, 'r', encoding='utf-8') as fin:
        for idx, line in enumerate(tqdm(fin)):
            line_split = line.split('\t')
            if len(line_split) == 3:
                query_lengths.append(len(nltk.word_tokenize(line_split[0])))
                passage_lengths.append(len(nltk.word_tokenize(line_split[1])))
            else:
                logging.error('This line has more than 3 fields: %s' % line)

            if sample_num and idx > sample_num:
                break

    query_lengths = np.array(query_lengths)
    passage_lengths = np.array(passage_lengths)
    #x = np.linspace(query_lengths.min(), query_lengths.max())

    plt.figure()
    #plt.hist(query_lengths, bins='auto', normed=True)
    plt.hist(query_lengths, bins=np.linspace(0, 70, 70), normed=True, cumulative=True)
    #plt.hist(query_lengths, bins='auto', normed=True, cumulative=True)

    if query_figure_path:
        plt.savefig(query_figure_path, dpi=300)
    else:
        plt.show()

    plt.figure()
    #plt.hist(passage_lengths, bins='auto', normed=True)
    plt.hist(passage_lengths, bins=np.linspace(0, 200, 200), normed=True, cumulative=True)
    #plt.hist(passage_lengths, bins='auto', normed=True, cumulative=True)
    if passage_figure_path:
        plt.savefig(passage_figure_path, dpi=300)
    else:
        plt.show()



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s')
    hist_statistics("/data/t-wulin/data/qna-data/deepqa-dev.tsv", 'query_lengths.png', 'passage_lengths.png')

