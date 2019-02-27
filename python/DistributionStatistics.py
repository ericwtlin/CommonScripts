# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def distribution_counter(num_array, interval, start=None, end=None, fig_path=None, cumulative=True):
    """
        if the num_array ranges from

    Args:
        num_array:
        start:
        end:
        interval:
        fig_path:
        cumulative:

    Returns:

    """
    num_array = np.array(num_array)
    if not start:
        start = np.min(num_array)
    if not end:
        end = np.max(num_array)

    plt.figure()
    split_num = (end - start) / interval
    plt.hist(num_array, bins=np.linspace(start, end, split_num), normed=True, cumulative=cumulative)
    # plt.hist(query_lengths, bins='auto', normed=True, cumulative=True)

    if fig_path:
        plt.savefig(fig_path, dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    nums = np.arange(0, 10, 0.1)
    print(nums)
    distribution_counter(nums, 0.5, 0, 10, cumulative=True)
    distribution_counter(nums, 0.5, 0, 10, cumulative=False)
    distribution_counter(nums, 0.5, cumulative=True)
    distribution_counter(nums, 0.5, cumulative=False)
