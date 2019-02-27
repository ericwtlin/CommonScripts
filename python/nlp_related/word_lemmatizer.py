# -*- coding: utf-8 -*-

import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok

import click
import codecs
import os
import re

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

class WordLemmatizer():
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def lemmatize(self, sentence):
        tokens = word_tokenize(sentence)
        tagged_sent = pos_tag(tokens)
        lemmas_sent = []
        for tag in tagged_sent:
            wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
            lemmas_sent.append(self.wnl.lemmatize(tag[0], pos=wordnet_pos))
        detokenizer = Detok()
        text = detokenizer.detokenize(lemmas_sent)
        text = re.sub('\s+,\s+', ', ', text)
        text = re.sub('\s+\.\s+', '. ', text)
        text = re.sub('\s+\?\s+', '? ', text)
        return text


@click.command()
@click.argument('input_tsv_path', type=click.STRING)
@click.argument('output_tsv_path', type=click.STRING)
@click.option('--col_idx', type=click.STRING, default="0")
@click.option('--in_place', type=click.BOOL, default=False)
def main(input_tsv_path, output_tsv_path, col_idx, in_place):
    print('input path: %s' % input_tsv_path)
    print('output path: %s' % output_tsv_path)
    print('col_idx: %s' % col_idx)
    col_indices = []
    for idx in col_idx.split(','):
        col_indices.append(int(idx))
        
    word_lemmatizer = WordLemmatizer()
    with codecs.open(input_tsv_path, 'r', encoding='utf-8') as fin:
        with codecs.open(output_tsv_path, 'w', encoding='utf-8') as fout:
            #for line in tqdm(fin):
            for line_idx, line in enumerate(fin):
                line = line.rstrip()
                line_split = line.split('\t')
                if in_place is False:
                    str_lemmatized = []
                    for idx in col_indices:
                        str_lemmatized.append(word_lemmatizer.lemmatize(line_split[idx]))
                    fout.write('%s\t%s%s' % (line, "\t".join(str_lemmatized), os.linesep))
                else:
                    for idx in col_indices:
                        line_split[idx] = word_lemmatizer.lemmatize(line_split[idx])
                    fout.write('%s%s' % ("\t".join(line_split), os.linesep))


if __name__ == '__main__':
    main()