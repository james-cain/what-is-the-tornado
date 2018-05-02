#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class UserLevelDao(base.DBBase):
    TableName = 'UserLevel'
    FieldLevel = 'UserLevel'
    FieldMoney = 'UpgradeMoney'

    def Query(self, level=None):
        sql = "select * from %s" % self.TableName
        if level:
            sql += " where %s = '%s' " % (self.FieldLevel, level)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            if level:
                return ret[0]
            return ret
        return None

if __name__ == '__main__':
    dao = UserLevelDao()
    print dao.QueryUserLevel()
