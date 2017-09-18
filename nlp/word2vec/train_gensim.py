# encoding=utf-8
# This script is validated on Python 2.7

import gensim
import logging
import os
import sys
import codecs
import pickle
import gzip
import argparse
from pprint import pprint
import multiprocessing as MP

logging.basicConfig(filename='logger.log', filemode='w', format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s', level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s'))
logging.getLogger().addHandler(console)


class MySentences(object):
    def __init__(self,filePath):
        self.filePath = filePath

    def __iter__(self):
        if os.path.isfile(self.filePath):
            for line in codecs.open(self.filePath,"r","utf-8"):
                line = line.strip()
                yield line.split("\t")
        else:
            logging.info("not file ", filePath)

def trainAndSave(args):
    inp, outp = args.path, args.out
    dim, binary, p_num = args.dim, args.binary, args.p_num
    logging.info("begin to load %s" %inp)
    sentences = MySentences(inp)
    logging.info("load %s finished,begin to train"  % inp)
    model = gensim.models.Word2Vec(sentences, size=dim,min_count=10,workers=p_num)
    logging.info("train finished,begin to dump model")
    #model.save_word2vec_format(outp, binary=binary)
    model.wv.save_word2vec_format(outp, binary=binary)
    logging.info("save model to %s suc" %outp)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("path",type=str, help="tokenized file path")
    parser.add_argument("--out",default="word2vec", type=str, help="write out word2vec name")
    parser.add_argument("--p_num",default=MP.cpu_count() - 2,type=int,help="parallel num [cpu_count - 2]")
    parser.add_argument("--dim", default= 200,type = int, help="word2vec dim [200]")
    parser.add_argument("--binary", default="False", type=str, help="save binary or not [False]")
    args = parser.parse_args()
    args.binary = args.binary in ["True", "Y", "true"]
    print(args)
    # input("xx:")

    trainAndSave(args)


