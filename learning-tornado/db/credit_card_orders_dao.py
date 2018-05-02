#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class CreditCardOrdersDao(base.DBBase):
    TableName = 'CreditCardOrders'
    FieldOrderNo = 'ApplyOrderNo'
    FieldUserId = 'UserId'
    FieldApplyTime = 'ApplyTime'
    FieldApplyBankNo = 'ApplyBankNo'

    BankTableName = 'BankInfo'
    FieldBankNo = 'BankNo'

    def Query(self, orderNo=None):
        sql = "select * from %s" % self.TableName
        if orderNo:
            sql += " where %s = '%s' " %s (self.FieldOrderNo, orderNo)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret[0]

    def QueryByUserId(self, userId):
        sql = "select * from %s inner join %s on %s=%s where %s='%s'" % (
            self.TableName, self.BankTableName, self.FieldBankNo,
            self.FieldApplyBankNo, self.FieldUserId, userId)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret

    def Insert(self, order):
        qmarks = ', '.join(['%s'] * len(order)) # 用于替换记录值
        cols = ', '.join(order.keys()) # 字段名
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.TableName, cols, qmarks)
        return self.Execute(sql, order.values())

    def Update(self, order):
        fields = []
        # update except id and no.
        for key in order.keys():
            if key != self.ApplyOrderNo:
                fields.append("%s='%s'" % (key, order[key]))
        fields = ', '.join(fields) # 字段名
        where = "%s='%s'" % (self.FieldOrderNo, order[self.FieldOrderNo])
        sql = "UPDATE %s SET %s where %s" % (self.TableName, fields, where)
        return self.Execute(sql)

    def delete(self, orderNo):
        where = "%s='%s'" % (self.FieldOrderNo, orderNo)
        sql = "DELETE from %s where %s" % (self.TableName, where)
        return self.Execute(sql)


