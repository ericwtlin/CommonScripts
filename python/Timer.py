# -*- coding: utf-8 -*-
"""
Timer

Authors:    Wutao Lin
Date:       17/11/30 下午12:06
"""
import time
import logging
import platform

class Timer(object):
    def __init__(self, unit='s'):
        """

        Args:
            unit:  's', 'ms'
        """
        self.anchors = []
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.system = 'unix'
        elif platform.system() == 'Windows':
            self.system = 'windows'
        logging.debug("System type: %s" % self.system)
        self.unit = unit

    def get_cur_time(self):
        """ get current time according to the unit
        Tips:
            According to :http://www.cnblogs.com/youxin/p/3157099.html, the precision of time.time()
             is better than time.clock() in Unix systems while time.clock() is better in Windows.

        Returns:
            current time stamp

        """
        times_of_unit = {
            's': 1,
            'ms': 1000,
        }
        if self.system == 'unix':
            return time.time() * times_of_unit[self.unit]
        elif self.system == 'windows':
            return time.clock() * times_of_unit[self.unit]

    def tick(self, description="", report_total=False):
        """ make notations at this time

        Args:
            description:  string


        Returns:

        """
        self.anchors.append({
            "time": self.get_cur_time(),
            "desc": description,
        })

        if len(self.anchors) > 1:
            if report_total is False:
                logging.info("%s, it has been %f %s since last tick." % \
                    (description, self.anchors[-1]['time'] - self.anchors[-2]['time'], self.unit))
            else:
                logging.info("%s, it has been %f %s since last tick and %f %s since the beginning." % \
                             (description, self.anchors[-1]['time'] - self.anchors[-2]['time'], self.unit,
                             self.anchors[-1]['time'] - self.anchors[0]['time'], self.unit))
        else:
            logging.info("%s, time established!" % description)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s')
    timer = Timer(unit='s')
    timer.tick("anchor 1")
    time.sleep(3)
    timer.tick("this is anchor 2")
    time.sleep(1)
    timer.tick("now something happens", report_total=True)


