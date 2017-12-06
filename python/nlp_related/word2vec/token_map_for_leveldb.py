#!/usr/bin/env python
# -*- coding:utf-8 -*-

import leveldb
import click
import tqdm
import pdb

@click.group()
def operate_group():
    pass

@operate_group.command()
@click.argument("word2vec", type=click.Path(exists=True))
@click.argument("db_name", type=click.Path(exists=False))
def creatdb(word2vec, db_name):
    file = open(word2vec)
    file.readline()

    db = leveldb.LevelDB(db_name)

    for line in tqdm.tqdm(file):
        word, vec = line.split(' ', 1)
        db.Put(word, vec.strip())

@operate_group.command()
@click.argument("key")
@click.argument("db_name", type=click.Path(exists=True))
def get_token(key, db_name):
    
    try:
        db = leveldb.LevelDB(db_name)
        print repr(db.Get(key))
    
    except:
        print '0.0 '*199 + '0.0'
    

if __name__ == '__main__':  
    
    if __name__ == "__main__":
        cli = click.CommandCollection(sources=[operate_group])

        cli()
