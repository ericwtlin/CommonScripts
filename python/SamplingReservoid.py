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

