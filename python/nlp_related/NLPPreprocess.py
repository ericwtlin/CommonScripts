#! -*- coding: utf-8 -*-
import logging
import cPickle as pkl
import codecs
import random
import math
import os
import time
import re
from random import randint


def full_to_half(s):
    # 全角转半角，返回unicode字符串
    n = []
    if type(s) == str:
        s = s.decode('utf-8')   #reformat to unicode
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = unichr(num)
        n.append(num)
    return ''.join(n)


def split_dataset(data, train_rate=0.8, valid_rate=0.1, test_rate=0.1):
    logging.info("total {} samples".format(len(data)))
    random.shuffle(data)
    train_valid_split_point = int(math.floor(len(data) * train_rate))
    valid_test_split_point = int(math.floor(len(data) * (train_rate+valid_rate)))

    training = data[:train_valid_split_point]
    validating = data[train_valid_split_point: valid_test_split_point]
    testing = data[valid_test_split_point:]
    return training, validating, testing


def load_embedding(embedding_path, embedding_dim):
    embedding_dict = dict()
    with codecs.open(embedding_path, 'r') as fin:
        _ = fin.readline()
        for line in fin:
            line = line.rstrip()
            word, vec = line.split(" ", 1)
            vector = [float(num) for num in vec.split(" ")]
            assert len(vector) == embedding_dim
            embedding_dict[word.decode('utf-8')] = vector
    return embedding_dict


