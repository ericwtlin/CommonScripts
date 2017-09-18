#encoding=utf-8

import os
import sys
import jieba
segmentor = None
try:
    from pyltp import Segmentor
    segmentor = Segmentor()
    segmentor.load("/home/bigdata/software/LTP/ltp_data/cws.model")
except ImportError:
    traceback.print_exc()

def tokenizer(s, segmentor, way="ltp"):
    s = s.strip()
    if way == "ltp":
        if segmentor is None:
            raise ValueError(segmentor)
        return ltpTokenizer(segmentor, s)
    elif way=="jieba":
        return jiebaTokenizer(s)

def ltpTokenizer(segmentor, s):
    words = segmentor.segment(s)
    words = list(words)
    return words

def jiebaTokenzier(s):
    return jieba.lcut(s)
