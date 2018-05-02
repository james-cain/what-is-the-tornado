#encoding=utf-8
import MySQLdb
import time

from DBUtils.PooledDB import PooledDB

# 单一连接的实现方式
class Base:
    def __init__(self, logger=None):
        self.logger = logger
        self._conn()

    def _conn (self):
        try:
            self.conn = MySQLdb.connect(host='localhost', user='kageweb', passwd='kageweb', charset="utf8")
            self.conn.select_db('kageweb')
            self.conn.set_character_set('utf8')
            return True
        except Exception, e:
            print e
            return False

    def _reConn (self,num = 28800,stime = 3):
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()
                _status = False
            except Exception, e:
                if self._conn()==True:
                    _status = False
                    break
                _number +=1
                time.sleep(stime)

    def GetConnection(self):
        self._reConn()
        return self.conn;

    def __del__(self):
        self.conn.close()

# 全局连接池
DBPool = PooledDB(MySQLdb, 15, host='localhost', user='kageweb', passwd='kageweb', charset="utf8mb4", db='kageweb')

class DBBase:
    def __init__(self, logger=None):
        self.logger = logger
        self.pool = DBPool

    def GetConnection(self):
        return self.pool.connection()

    def ExecuteResult(self, sql, values=None):
        try:
            conn = self.GetConnection()
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            try:
                cursor.execute(sql, values)
                return cursor.fetchall()
            except Exception, e:
                if self.logger:
                    self.logger.error("%s execute error[%s], SQL error: %s" % (__file__, sql, str(e)))
                return None
            finally:
                cursor.close()
                conn.close()
        except Exception, e:
            if self.logger:
                self.logger.error("%s connect error: %s" % (__file__, str(e)))

    def Execute(self, sql, values=None):
        try:
            conn = self.GetConnection()
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            try:
                cursor.execute(sql, values)
                conn.commit()
                return True
            except Exception, e:
                if self.logger:
                    self.logger.error("%s excecute error[%s], SQL error: %s" % (__file__, sql, str(e)))
                return False 
            finally:
                cursor.close()
                conn.close()
        except Exception, e:
            if self.logger:
                self.logger.error("%s connect error: %s" % (__file__, str(e)))
            return False

if __name__ == '__main__':
    pool = PooledDB(MySQLdb, 15, host='localhost', user='kageweb', passwd='kageweb', charset="utf8", db='kageweb')
    db = pool.connection()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('select * from User');
    res = cur.fetchall()
    cur.close()
    db.close()
    print res

