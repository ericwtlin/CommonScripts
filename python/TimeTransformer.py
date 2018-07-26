#! -*- coding: utf-8 -*-
# @Time    : 18-7-27
# @Author  : Wutao Lin
# @Environment : Python 3.5
# @function: Conduct the transformation among string, time and datetime


import time
import datetime
import platform

class TimeTransformer():
    def __init__(self):
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.system = 'unix'
        elif platform.system() == 'Windows':
            self.system = 'windows'

    def get_cur_timestamp(self):
        if self.system == 'unix':
            return time.time()
        elif self.system == 'windows':
            return time.clock()


    def get_cur_datetime(self):
        return datetime.datetime.now()


    def transform_string_to_datetime(self, datetime_str):
        """

        Args:
            datetime_str: e.g. '2015-08-28 16:43:37'

        Returns:
            datetime obj
        """
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


    def transform_string_to_timestamp(self, datetime_str):
        """

        Args:
            datetime_obj:

        Returns:
            timestamp

        """
        return time.mktime(self.transform_string_to_timetuple(datetime_str))


    def transform_string_to_timetuple(self, datetime_str):
        """

        Args:
            datetime_str: e.g. '2015-08-28 16:43:37'

        Returns:
            time.struct_time,
                e.g. time.struct_time(tm_year=2008, tm_mon=11, tm_mday=10, tm_hour=17, tm_min=53, tm_sec=59, tm_wday=0, tm_yday=315, tm_isdst=-1)

        """
        return time.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


    def transform_datetime_to_string(self, datetime_obj):
        """

        Args:
            datetime_obj:

        Returns:
            e.g. '2015-08-28 16:43:37'

        """
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


    def transform_datetime_to_timestamp(self, datetime_obj):
        """

        Args:
            datetime_obj:

        Returns:
            time stamp

        """
        return time.mktime(datetime_obj.timetuple())


    def transform_datetime_to_timetuple(self, datetime_obj):
        """

        Args:
            datetime_obj:

        Returns:
            time.struct_time,
                e.g. time.struct_time(tm_year=2008, tm_mon=11, tm_mday=10, tm_hour=17, tm_min=53, tm_sec=59, tm_wday=0, tm_yday=315, tm_isdst=-1)

            You can get year by timetuple.tm_year, get month by timetuple.tm_mon

        """
        return datetime_obj.timetuple()


    def transform_timestamp_to_datetime(self, timestamp_obj):
        """

        Args:
            timestamp_obj:

        Returns:
            datetime obj

        """
        return datetime.datetime.fromtimestamp(timestamp_obj)


    def transform_timestamp_to_string(self, timestamp_obj):
        """

        Args:
            timestamp_obj:

        Returns:
            '2015-08-28 16:43:37'

        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_obj))

    def transform_timestamp_to_string(self, timestamp_obj):
        """

        Args:
            timestamp_obj:

        Returns:
            '2015-08-28 16:43:37'

        """
        return timestamp_obj


    def transform_timestamp_to_timetuple(self, timestamp_obj):
        """

        Args:
            timestamp_obj:

        Returns:
            time.struct_time,
                e.g. time.struct_time(tm_year=2008, tm_mon=11, tm_mday=10, tm_hour=17, tm_min=53, tm_sec=59, tm_wday=0, tm_yday=315, tm_isdst=-1)

            You can get year by timetuple.tm_year, get month by timetuple.tm_mon

        """
        return self.transform_timestamp_to_datetime(timestamp_obj).timetuple()


    def get_time_ago(self, days_ago=0, hours_ago=0, minutes_ago=0, seconds_ago=0, weeks_ago=0):
        """ get some time ago

        Args:
            days_ago:
            hours_ago:
            minutes_ago:
            seconds_ago:

        Returns:
            datetime

        """
        return datetime.datetime.now() - datetime.timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago, seconds=seconds_ago, weeks=weeks_ago)



if __name__ == '__main__':
    time_transformer = TimeTransformer()

    time_stamp_now = time_transformer.get_cur_timestamp()
    print('timestamp now:' + repr(time_stamp_now))
    datetime_now = time_transformer.get_cur_datetime()
    print('datetime now:' + repr(datetime_now))

    # timestamp -> datetime
    dt = time_transformer.transform_timestamp_to_datetime(time_stamp_now)
    print('datatime:' + repr(dt))
    # timestamp -> string
    s = time_transformer.transform_timestamp_to_string(time_stamp_now)
    print('s:' + repr(s))

    # datetime -> timestamp
    ts = time_transformer.transform_datetime_to_timestamp(dt)
    print('timestamp:' + repr(ts))
    # datetime -> string
    s = time_transformer.transform_datetime_to_string(dt)
    print('s:' + repr(s))

    # string -> timetuple
    ts = time_transformer.transform_string_to_timetuple(s)
    print('timetuple:' + repr(ts))
    # string -> datetime
    dt = time_transformer.transform_string_to_datetime(s)
    print('datatime:' + repr(dt))

    # get 3 days ago
    dt_3days_ago = time_transformer.get_time_ago(days_ago=3)
    print('datetime:' + repr(dt_3days_ago))


