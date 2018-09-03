#! -*- coding: utf-8 -*-
import logging
import pickle as pkl
import codecs
import random
import math
import os
import time
import re
from random import randint
import click

class SamplingReservoid:
    def __init__(self, sample_num):
        self.sample_num = sample_num
        self.total_count = 0
        self.reservoid = []

    def add_sample(self, sample):
        self.total_count += 1
        if len(self.reservoid) < self.sample_num:
            self.reservoid.append(sample)
        else:
            if random.random() <= self.sample_num * 1.0 / self.total_count:
                ind = random.randint(0, self.sample_num - 1)
                self.reservoid[ind] = sample

    def get_sample_result(self):
        return self.reservoid

    def is_enough(self):
        """if the total count is enough for assumed sample num

        Returns:
            True: total count larger than assumed sample num
            False: total count less than assumed sample num

        """
        if self.total_count < self.sample_num:
            return False
        else:
            return True


@click.command()
@click.argument('input_path', type=click.STRING)
@click.argument('output_path', type=click.STRING)
@click.argument('sample_num', type=click.INT)
def main(input_path, output_path, sample_num):
    sampler = SamplingReservoid(sample_num)
    with codecs.open(input_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sampler.add_sample(line)

    with codecs.open(output_path, 'w', encoding='utf-8') as fout:
        for line in sampler.get_sample_result():
            fout.write(line)


if __name__ == '__main__':
    main()

