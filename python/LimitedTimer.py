
import time
import re

class  LimitedTimer(object):
    """
    限时运行，超时退出
    """
    def __init__(self, due_time):
        """
        样例：
            limited_timer = LimitedTimer('11:09:40')
            limited_timer = LimitedTimer('2018-06-03 11:10:15')
            limited_timer = LimitedTimer(0.001)

        Args:
            due_time: 
                如果格式为时间点，那么超出该时间点到期， 格式可以为'%H:%M:%S' or '%Y-%m-%d %H:%M:%S', 如果为指定年月日，默认当前日
                如果格式为一个浮点数n，那么指限定n小时
        """
        if isinstance(due_time, str):
            # 时间点
            if due_time.find('-') == -1:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                due_time = localtime.split()[0] + ' ' + due_time  # 取当前这天

            self.__due_time = due_time
            self.__due_time_stamp = time.mktime(time.strptime(due_time, '%Y-%m-%d %H:%M:%S'))
        else:
            # 时长
            self.__due_time_stamp = time.time() + due_time * 3600
            self.__due_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.__due_time_stamp))


    def due(self):
        """

        Returns:
            已超时，返回True，否则返回False

        """
        if time.time() >= self.__due_time_stamp:
            return True
        else:
            return False

    def get_due_time(self):
        """

        Returns:
            '%Y-%m-%d %H:%M:%S'

        """
        return self.__due_time

if __name__ == '__main__':
    limited_timer = LimitedTimer('11:09:40')
    # limited_timer = LimitedTimer('2018-06-03 11:10:15')
    #limited_timer = LimitedTimer(0.001)

    while True:
        flag = limited_timer.due()
        print(flag)
        if flag:
            break
        else:
            time.sleep(1)