#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class UserMoneyRecordDao(base.DBBase):
    TableName = 'UserMoneyRecord'
    FieldUserId = 'UserId'
    FieldType = 'Type' # 0 下级升级产生
    FieldBalance = 'Balance'
    FieldTime = 'Time'
    FieldRemark = 'Remark'
    def Insert(self, UserId, Type, Balance, Remark):
        # record 自增
        record = {
            self.FieldUserId: UserId,
            self.FieldType:Type,
            self.FieldBalance: Balance,
            self.FieldRemark:Remark,
            self.FieldTime: int(time.time())
        }
        qmarks = ', '.join(['%s'] * len(record)) # 用于替换记录值
        cols = ', '.join(record.keys()) # 字段名
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.TableName, cols, qmarks)
        return self.Execute(sql, record.values())

    def QueryByUserId(self, userId):
        sql = "select * from %s where %s='%s'" %s (self.TableName, self.FieldUserId, userId)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret
        else:
            return None

if __name__ == '__main__':
    dao = UserMoneyRecordDao()
    print dao.Insert('123', 0, -10, '下级会员升级')
