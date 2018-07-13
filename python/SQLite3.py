import sqlite3
import logging

"""
SQLite 3 operator

Environment: Python 3.6
"""


class SQLite3(object):
    def __init__(self, db_path):
        try:
            self.db = sqlite3.connect(db_path)
            self.cursor = self.db.cursor()
        except Exception as e:
            logging.error("Mysql Error %s" % (e))

    def __del__(self):
        self.close()

    def create_table(self, sql):
        """
        
        Args:
            sql:  the create table command

        Returns:

        """
        self.exceute_sql(sql)

    def query(self, sql):
        try:
            ret = self.cursor.execute(sql)
        except Exception as e:
            ret = -1
            logging.info("Select command %s error info: %s" % (sql, e))
        return ret

    def fetch_row(self):
        """ Fetch a row
        
        Returns:
            None / dict： e.g. {'age': xxx, 'salary': xxx}

        """
        try:
            result = self.cursor.fetchone()
            desc = self.cursor.description
            ret = {}
            for i in range(0, len(result)):
                ret[desc[i][0]] = result[i]
        except:
            ret = None
        return ret

    def fetch_all(self):
        """ Fetch all rows

        Returns:
            None / list of dicts： e.g. [{'age': xxx, 'salary': xxx}, ...]

        """
        try:
            result = self.cursor.fetchall()
            desc = self.cursor.description
            ret = []
            for inv in result:
                _d = {}
                for i in range(0, len(inv)):
                    _d[desc[i][0]] = inv[i]
                ret.append(_d)
        except:
            ret = None
        return ret

    def insert(self, sqls):
        """ insert
        注意！在这个情况下，不论是整数、浮点数，模板都应该用%s，而不是%d或%f
        Args:
            table_name: 
            sql: e.g. "INSERT INTO trade (name, account, saving) VALUES ( %s, %s, %s )"
            values: list or nested list.  e.g. ('雷军', '13512345678', 10000) or [('雷军', '13512345678', 10000), ('雷军', '13512345678', 10000), ...]
            
        Returns:
            
        """
        if isinstance(sqls, list):
            # multiple rows
            try:
                for sql in sqls:
                    self.cursor.execute(sql)
                ret = 0
                self.commit()
            except Exception as e:
                ret = -1
                self.rollback()
                logging.error("Insert error sql:%s; error info: %s" % (sql, e))
        else:
            # single row
            try:
                ret = self.cursor.execute(sqls)
                self.commit()
            except Exception as e:
                ret = -1
                self.rollback()
                logging.error("Insert error sql:%s; error info: %s" % (sqls, e))
        return ret

    def exceute_sql(self, sql):
        """ update or delete data
        
        Args:
            sql: complete sql command

        Returns:

        """
        try:
            ret = self.cursor.execute(sql)
            self.commit()
        except Exception as e:
            ret = -1
            logging.error("Excute command error sql: %s, error info; %s" % (sql, e))
            self.db.rollback()

        return ret

    def update(self, sql):
        return self.exceute_sql(sql)

    def delete(self, sql):
        return self.exceute_sql(sql)

    '''
    def get_last_insert_id(self):
        return self.cursor.lastrowid

    def rowcount(self):
        return self.cursor.rowcount
    '''

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        if hasattr(self, 'db'):
            self.db.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s')
    db = SQLite3('test.db')
    create_table_sql = '''CREATE TABLE record 
        (ID INT PRIMARY KEY,
         enterpriseName text    not null,
         url text,
         status int
         );
        '''

    # status: 0:已爬取； 1：搜索不到； 2：页面解析错误/被反爬等

    db.create_table(create_table_sql)

    '''
    insert_sql = 'INSERT INTO record (ID, enterpriseName, url, status) VALUES (null, "%s", "%s", "%s")'
    insert_sqls = []
    for insert_value in [('company1',  'http://asdfasdf', 0), ('company2',  'http://asdfasdf', 1)]:
        sql = insert_sql % insert_value
        insert_sqls.append(sql)
    #insert_values = ('company1', '1111', '1112', '1113')
    db.insert(insert_sqls)

    db.query('SELECT * from record')
    data = db.fetch_all()
    #data = db.fetch_row()
    logging.info(data)

    db.delete('DELETE from record where enterpriseName="company1"')

    db.update('update record set status = 2 where status=1')
    db.query('SELECT * from record')
    data = db.fetch_all()
    # data = db.fetch_row()
    logging.info(data)
    '''



