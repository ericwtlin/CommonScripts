# -*- coding: utf-8 -*-
"""
MySQL operator

Environment: Python 3.6

Tips:
1. 如果要插入NULL，那么直接在values参数里面给Python的None就可以了
2. cursor.excute(sql, values)这种格式的语句中，不论values是字符串、整数、小数，占位符都给%s
"""

import pymysql
import logging
import traceback
import platform
import time
import datetime



class MySQL(object):
    def __init__(self, host, user, password, database, port=3306, charset="utf8", reconnect_interval=3600):
        """

        Args:
            host:
            user:
            password:
            database:
            port:
            charset:
            reconnect_interval: 单位：秒，每达到reconnect_interval秒，就重新连接数据库，否则容易有数据库断开报错的问题
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.reconnect_interval = reconnect_interval
        self.connect()

        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.system = 'unix'
        elif platform.system() == 'Windows':
            self.system = 'windows'

        self.last_reconnect_time = self.get_time()

    def __del__(self):
        self.close()

    def connect(self):
        while True:
            try:
                self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.database, charset=self.charset)
            except Exception as e:
                logging.error("Mysql Error %s" % (e))
            break

    def close(self):
        if hasattr(self, 'db'):
            self.db.close()

    def get_time(self):
        if self.system == 'unix':
            return time.time()
        elif self.system == 'windows':
            return time.clock()

    def check_reconnect(self):
        """ 检查是否需要重新连接

        Returns:

        """
        try:
            self.db.ping()
        except Exception as e:
            logging.error('%s, Mysql断开，重连' % e)
            self.connect()

        time_now = self.get_time()
        if time_now - self.last_reconnect_time > self.reconnect_interval:
            logging.info('达到重连间隔%d秒，重连' % self.reconnect_interval)
            self.close()
            self.connect()
            self.last_reconnect_time = time_now

    def query(self, sql, values, fetch_all=True, reformat=True):
        """ select查询，并且完成fetch操作，返回fetch的结果
        tips:
            fetch操作仅支持两种，要么全部fetch，要么只fetch 1个。对于fetch少量的做法，应该在select语句中用limit限定，而不应该在此限定

        Args:
            sql:
            values:
            fetch_all: True则fetch all，False则fetch one
            reformat: whether to return a formatted dictionary or origin result

        Returns:
            如果无结果，则返回None
            如果有结果:
                如果reformat=True, 则返回的每个条目都转换成dict。  e.g. {'age': xxx, 'salary': xxx}
                如果reformat=False, 则返回的每个条目都是mysql的默认返回样式
                如果fetch_all=True，则返回多个项，保存在列表里。
                如果fetch_all=False，则返回只有一个项，不以列表包裹。
        """
        self.check_reconnect()
        try:
            while True:
                try:
                    with self.db.cursor() as cursor:
                        cursor.execute(sql, values)
                        ret = self.fetch_data(cursor, fetch_all=fetch_all, reformat=reformat)
                    break
                except TimeoutError as toe:
                    logging.error('%s, MySQL Timeout, reconnect...' % (toe))
                    self.connect()
        except Exception as e:
            ret = None
            logging.info("Select command %s error info: %s" % (sql, e))
        return ret

    def query_flexible(self, sql, fetch_all=True, reformat=True):
        """ select查询，且完成fetch操作，返回fetch的结果
        
        tips:
            fetch操作仅支持两种，要么全部fetch，要么只fetch 1个。对于fetch少量的做法，应该在select语句中用limit限定，而不应该在此限定

        Args:
            sql: 这里sql是一个完整的sql语句，用于更加灵活的查询
            values:
            fetch_all: True则fetch all，False则fetch one
            reformat: whether to return a formatted dictionary or origin result

        Returns:
            如果无结果，则返回None
            如果有结果:
                如果reformat=True, 则返回的每个条目都转换成dict。  e.g. {'age': xxx, 'salary': xxx}
                如果reformat=False, 则返回的每个条目都是mysql的默认返回样式
                如果fetch_all=True，则返回多个项，保存在列表里。
                如果fetch_all=False，则返回只有一个项，不以列表包裹。
        """
        self.check_reconnect()
        try:
            while True:
                try:
                    with self.db.cursor() as cursor:
                        cursor.execute(sql)
                        ret = self.fetch_data(cursor, fetch_all=fetch_all, reformat=reformat)
                    break
                except TimeoutError as toe:
                    logging.error('%s, MySQL Timeout, reconnect...' % (toe))
                    self.connect()
        except Exception as e:
            ret = None
            logging.info("Select command %s error info: %s" % (sql, e))
        return ret

    def fetch_data(self, cursor, fetch_all=True, reformat=True):
        """ 在cursor完成select查询后，取回查询结果
        
        Args:
            cursor: 
            fetch_all: True则fetch all，False则fetch one
            reformat: whether to return a formatted dictionary or origin result

        Returns:
            如果无结果，则返回None
            如果有结果:
                如果reformat=True, 则返回的每个条目都转换成dict。  e.g. {'age': xxx, 'salary': xxx}
                如果reformat=False, 则返回的每个条目都是mysql的默认返回样式
                如果fetch_all=True，则返回多个项，保存在列表里。
                如果fetch_all=False，则返回只有一个项，不以列表包裹。

        """
        try:
            if fetch_all:
                result = cursor.fetchall()
                if reformat:
                    desc = cursor.description
                    ret = []
                    for inv in result:
                        _d = {}
                        for i in range(0, len(inv)):
                            _d[desc[i][0]] = inv[i]
                        ret.append(_d)
                else:
                    ret = result
            else:
                result = cursor.fetchone()
                if reformat:
                    desc = cursor.description
                    ret = {}
                    for i in range(0, len(result)):
                        ret[desc[i][0]] = result[i]
                else:
                    ret = result
        except Exception as e:
            ret = None
        return ret

    def insert(self, sql, values):
        """ insert
        注意！在这个情况下，不论是整数、浮点数，模板都应该用%s，而不是%d或%f
        Args:
            table_name: 
            sql: e.g. "INSERT INTO trade (name, account, saving) VALUES ( %s, %s, %s )"
            values: list or nested list.  e.g. ('雷军', '13512345678', 10000) or [('雷军', '13512345678', 10000), ('雷军', '13512345678', 10000), ...]
            
        Returns:
            
        """
        self.check_reconnect()
        if isinstance(values[0], list) or isinstance(values[0], tuple):
            # multiple rows
            try:
                while True:
                    try:
                        with self.db.cursor() as cursor:
                            ret = cursor.executemany(sql, values)
                        self.commit()
                        break
                    except TimeoutError as toe:
                        logging.error('%s, MySQL Timeout, reconnect...' % (toe))
                        self.connect()
            except Exception as e:
                ret = -1
                self.rollback()
                logging.error("Insert error sql:%s  data_sample: %s; error info: %s; error trace: %s" % (sql, values[0], e, traceback.format_exc()))
        else:
            # single row
            try:
                while True:
                    try:
                        with self.db.cursor() as cursor:
                            ret = cursor.execute(sql, values)
                        self.commit()
                        break
                    except TimeoutError as toe:
                        logging.error('%s, MySQL Timeout, reconnect...' % (toe))
                        self.connect()
            except Exception as e:
                ret = -1
                self.rollback()
                logging.error("Insert error sql: %s  data_sample: %s; error info: %s, error trace: %s" % (sql, values, e, traceback.format_exc()))
        return ret

    def insert_by_dict(self, table_name, info):
        """ 推荐！通过字典中保存数据库列和值的形式插入, 一次只能插入1条
        推荐用这个方法而不用self.insert()，因为self.insert()方法在字段很多的时候，很繁琐，增减字段时非常麻烦
        
        Args:
            table_name: 
            info: dict like: {'col1': 'value1': 'col2': 'value2'}

        Returns:

        """
        self.check_reconnect()
        cols = list(info.keys())
        values = [info[col] for col in cols]
        insert_sql ="INSERT INTO " + table_name + " (%s) VALUES ( " % (','.join(cols)) +  ','.join(['%s'] * len(values)) + ")"
        return self.insert(insert_sql, values)

    def update_or_delete(self, sql, values):
        """ update or delete data

        Args:
            sql: complete sql command, %s两边需要加引号

        Returns:
            -1: failed;
            >0: success

        """
        self.check_reconnect()
        try:
            while True:
                try:
                    with self.db.cursor() as cursor:
                        ret = cursor.execute(sql, values)
                    self.commit()
                    break
                except TimeoutError as toe:
                    logging.error('%s, MySQL Timeout, reconnect...' % (toe))
                    self.connect()
        except Exception as e:
            ret = -1
            logging.error("Update_or_delete error sql: %s, error info; %s, error trace: %s" % (sql, e, traceback.format_exc()))
            self.rollback()

        return ret

    def update(self, sql, values):
        return self.update_or_delete(sql, values)

    def update_by_dict(self, table_name, info, condition_str):
        """ 用dict形式更新数据
        
        Args:
            table_name: 
            info: dict like: {'col1': 'value1': 'col2': 'value2'}
            condition_str: str， 不包括'where '

        Returns:

        """
        cols = list(info.keys())
        values = [info[col] for col in cols]
        update_sql = 'UPDATE ' + table_name + ' set ' + ','.join(['%s=' % col + '%s' for col in cols]) + ' where ' + condition_str + ';'
        return self.update(update_sql, values)

    def delete(self, sql, values):
        return self.update_or_delete(sql, values)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s')
    db = MySQL('123.56.188.183', 'develop', 'develop1212', 'toulian', port=4091)
    '''
    insert_sql = 'INSERT INTO debug_enterprise (enterpriseName, unifiedSocialCreditCode, registerNumber, organizationCode) VALUES (%s, %s, %s, %s)'
    insert_values = [('company1', '1111', '1112', '1113'), ('company2', '2221', '2222', '2223')]
    #insert_values = ('company1', '1111', '1112', '1113')
    db.insert(insert_sql, insert_values)

    db.query('SELECT * from debug_enterprise where enterpriseName="company1"')
    data = db.fetch_all()
    #data = db.fetch_row()
    logging.info(data)

    db.delete('DELETE from debug_enterprise where enterpriseName="company1"')

    db.update('update debug_enterprise set unifiedSocialCreditCode = 555 where id = 2')
    '''
    #insert_sql = 'INSERT INTO debug_enterprise (enterpriseName, registerNumber, dateOfEstablishment, approvedDate) VALUES (%s, %s, %s, %s)'
    #db.insert(insert_sql, ['company223', '00001', '无固定期限', '2016-05-10 10:01:02'])

    '''
    insert_sql = 'INSERT INTO t_enterprise_detail_crawl_log (enterpriseName,crawlStatus,url) VALUES ( %s,%s,%s)'
    insert_values = ['北京忠诚恒兴投资管理有限公司', -2, 'https://www.qichacha.com/firm_61f2708c5224d440cf971d5fe03b75b6.html']
    db.insert(insert_sql, insert_values)
    '''

    select_sql = 'select * from t_enterprise where enterpriseName=%s ' \
                                                           'or enterpriseName=%s or unifiedSocialCreditCode=%s'
    values = ("北京中鸿医疗卫生健康产业研究中心", "北京中鸿医疗卫生健康产业研究中心", '52110000MJ0163191U')
    data = db.query(select_sql, values, fetch_all=True, reformat=True)[0]
    crawlTime = data['crawlTime']
    print(crawlTime)
    baseline_time = datetime.datetime.combine(datetime.date(2018, 6, 21), datetime.time(12, 0, 0))
    if crawlTime > baseline_time:
        print('bigger')
    else:
        print('smaller')




