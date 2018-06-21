import pymysql
import logging

class MySQL(object):
    def __init__(self, host, user, password, database, port=3306, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        try:
            self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=database, charset=self.charset)
            self.cursor = self.db.cursor()
        except Exception as e:
            logging.error("Mysql Error %s" % (e))

    def __del__(self):
        self.close()

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

    def insert(self, sql, values):
        """ insert
        
        Args:
            table_name: 
            sql: e.g. "INSERT INTO trade (name, account, saving) VALUES ( %s, %s, %.2f )"
            values: list or nested list.  e.g. ('雷军', '13512345678', 10000) or [('雷军', '13512345678', 10000), ('雷军', '13512345678', 10000), ...]
            
        Returns:
            
        """
        if isinstance(values[0], list) or isinstance(values[0], tuple):
            # multiple rows
            try:
                ret = self.cursor.executemany(sql, values)
                self.commit()
            except Exception as e:
                ret = -1
                self.rollback()
                logging.error("Insert error sql:%s  data_sample: %s; error info: %s" % (sql, values[0], e))
        else:
            # single row
            try:
                ret = self.cursor.execute(sql, values)
                self.commit()
            except Exception as e:
                ret = -1
                self.rollback()
                logging.error("Insert error sql: %s  data_sample: %s; error info: %s" % (sql, values, e))
        return ret

    def update_or_delete(self, sql):
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
            logging.error("Update_or_delete error sql: %s, error info; %s" % (sql, e))
            self.db.rollback()

        return ret

    def update(self, sql):
        return self.update_or_delete(sql)

    def delete(self, sql):
        return self.update_or_delete(sql)

    def get_last_insert_id(self):
        return self.cursor.lastrowid

    def rowcount(self):
        return self.cursor.rowcount

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        if hasattr(self, 'db'):
            self.db.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d: %(message)s')
    db = MySQL('', '', '', '', port=123456)
    
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
    
    insert_sql = 'INSERT INTO debug_enterprise (enterpriseName, registerNumber, dateOfEstablishment, approvedDate) VALUES (%s, %s, %s, %s)'
    db.insert(insert_sql, ['company111', '0000', '2016-05-10', '2016-05-10 10:01:02'])

