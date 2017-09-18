#encoding=utf-8

import codecs
import os
import sys
import logging
import argparse
import time
import math
import traceback
import multiprocessing as MP
from datetime import datetime
from segment import tokenizer
segmentor = None
try:
    from pyltp import Segmentor
    segmentor = Segmentor()
    segmentor.load("/home/liyi193328/software/LTP/ltp_data/cws.model")
except ImportError:
    traceback.print_exc()
    raise Exception()

logFormatter = logging.Formatter("%(levelname)s;%(funcName)s;pro-%(process)d;lineth-%(lineno)s:%(message)s --- %(asctime)s;", 
                                datefmt="%Y-%m-%d %H:%M:%S")
rootLogger = logging.getLogger()
fileHandler = logging.FileHandler("{0}/{1}.log".format("./", "tokenFiles"))
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.DEBUG)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
rootLogger.addHandler(consoleHandler)

# logging.basicConfig(format="%(levelname)s;%(funcName)s;pro-%(process)d;lineth-%(lineno)s:%(message)s --- %(asctime)s;", level = logging.DEBUG,
#                     datefmt="%Y-%m-%d %H:%M:%S", )

# logging.basicConfig(level=logging.DEBUG)

def gen_partion_ranges(sz, partion_num):  ##parthion_num: 总的切分数， sz: 长度
    sz, partion_num = int(sz), int(partion_num)
    partion_size = math.ceil(sz/partion_num)
    for i in range(partion_num):
        be = i * partion_size
        en = i * partion_size + partion_size
        be = int(be)
        en = int(en)
        yield be, en

def gen_batch(sz, batch_size):  ##返回长度为sz，大小为batch_size的[be,en)迭代器
    assert type(sz) == int
    assert type(batch_size) == int
    import math
    partion = math.ceil( sz / batch_size )  #ceil(5/2) = 3
    for i in range(partion):
        be = i * batch_size
        en = min(i*batch_size + batch_size, sz)
        yield int(be), int(en)

def tokenLines(be, en, lines, way="ltp"):
    rootLogger.info("start with index from {} to {}".format(be, en) )
    result = []
    for line in lines:
        words = tokenizer(line, segmentor, way)
        result.append(words)
    return result

def tokenFile(path, newP, p_num=1, way="ltp"):
    p_num = min(MP.cpu_count(), p_num)
    rootLogger.info(locals())
    pool = MP.Pool(p_num)
    f = codecs.open(path, "r", "utf-8")
    lines = f.readlines()
    rootLogger.info("all lines num: {}".format(len(lines)))
    # input("xx:")
    L = len(lines)
    stPairs = gen_partion_ranges(L, p_num)
    pro = []
    result = []
    for i, (be, en) in enumerate(stPairs):
        p = pool.apply_async(tokenLines, args=(be, en, lines[be:en]), kwds={"way":way})
        pro.append(p)

    for i, p in enumerate(pro):
        result.extend(p.get())

    pool.close()
    pool.join()

    rootLogger.info("get all results, begin to write to file {}".format(newP))

    fp = codecs.open(newP, "w", "utf-8")
    for words in result:
        line = "\t".join(words) + "\n"
        fp.write(line)
    fp.close()

def splitOneFile(path, partition=10,suffix=".part"):
    assert os.path.isfile(path), path
    with codecs.open(path,"r", "utf-8") as f:
        lines = f.readlines()
        L = len(lines)
        cnt = 0
        for be, en in gen_partion_ranges(L, partition):
            newP = path + suffix + str(cnt)
            for line in lines[be:en]:
                f.write(line.strip()+"\n")

def filterFunc(s):
    if ".token" in s:
        return True
    return False

def merge(dir,filterFunc,mFilePath="all.merge"):
    assert os.path.isdir(dir), dir
    path_list = [os.path.join(dir, d) for d in os.listdir(dir)]
    path_list = [x for x in path_list if filterFunc(x)]
    rootLogger.info("total {} files".format(len(path_list)))
    rootLogger.info("writing to {}".format(mFilePath))
    with codecs.open(mFilePath,"w", "utf-8") as f:
        for i, path in enumerate(path_list):
            rootLogger.info("mergeing {}".format(path))
            with codecs.open(path, "r","utf-8") as fp:
                lines = fp.readlines()
                for line in lines:
                    f.write(line.strip() + "\n")

def tokenDir(dir, newDir = "./", p_num=1, way="ltp",suffix=".token"):
    if os.path.exists(newDir) == False:
        os.mkdir(newDir)
    if os.path.isdir(dir) == True:
        path_list = [os.path.join(dir, d) for d in os.listdir(dir)]
        for i, xp in enumerate(path_list):
            rootLogger.info("now handleing {}".format(xp))
            fname = os.path.basename(xp)
            newP = os.path.join(newDir, fname + suffix )
            if os.path.exists(newP) == True:
                rootLogger.info("{} exists, continue".format(newP))
                continue
            tokenFile(xp, newP, p_num=p_num, way=way)
    else:
        tokenFile(path, path + suffix, p_num=p_num, way=way)

if __name__ == '__main__':
    now0 = datetime.now()
    rootLogger.info("begin_time: %s"%(now0))
    time.sleep(3)
    words = tokenizer("我爱中华人民共和国", segmentor)
    print(words)
    # input("xx:")
    parser = argparse.ArgumentParser()
    parser.add_argument("path",type=str, help="原始文件路径")
    parser.add_argument("newP",type=str, help="write file path")
    parser.add_argument("--p_num",default=MP.cpu_count() - 2,type=int,help="parallel num [cpu_count - 2]")
    parser.add_argument("--s_way", default= "ltp",type=str, help="segment way,ltp|jieba [ltp]")
    args = parser.parse_args()
    # tokenFile(args.path, args.newP, p_num = args.p_num, way=args.s_way)
    tokenDir(args.path, args.newP, p_num = args.p_num, way=args.s_way)
    merge(args.newP, filterFunc, "../baike_words.merge")
    now1 = datetime.now()
    rootLogger.info("end_time: %s" %(now1))
    t = now1 - now0
    secs = t.total_seconds()
    rootLogger.info("total cost minutes: %s\n" %(float(secs)/60.0) )


