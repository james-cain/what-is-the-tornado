#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class UserUpgradeOrderDao(base.DBBase):
    TableName = 'UserUpgradeOrder'
    FieldUserId = 'UserId'
    FieldOrderId = 'OrderId'
    FieldOrderState = 'OrderState'
    FieldAddTime = 'OrderAddTime'
    FieldModifyTime = 'OrderModifyTime'
    FieldOrigin = 'OriginUserLevel'
    FieldUpgrade = 'UpgradeUserLevel'
    FieldMoney = 'OrderMoney'

    def Query(self, orderId):
        sql = "select * from %s where %s = '%s'" % (self.TableName, self.FieldOrderId, orderId)
        ret = self.ExecuteResult(sql)
        if ret:
            return ret[0]

    def QueryByUserId(self, userId):
        sql = "select * from %s where %s = '%s'" % (self.TableName, self.FieldUserId, userId)
        ret = self.ExecuteResult(sql)
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
            if key == self.FieldOrderState or key == self.FieldModifyTime:
                fields.append("%s='%s'" % (key, order[key]))
        if len(fields) == 0:
            return False
        fields = ', '.join(fields) # 字段名
        where = "%s='%s'" % (self.FieldOrderId, order[self.FieldOrderId])
        sql = "UPDATE %s SET %s where %s" % (self.TableName, fields, where)
 
        return self.Execute(sql)

    def Delete(self, orderId):
        sql = "delete from %s where %s = '%s'" % (self.TableName, self.FieldOrderId, orderId)
        return self.Execute(sql)

if __name__ == '__main__':
    dao = UserUpgradeOrderDao()
    orderId = '4123432143214231'
    order = {'UserId': '8aa3ef66-2ad0-11e8-afc5-00163e0309bf', 'OrderAddTime': '14321432', 'OrderModifyTime': '23423', 'OriginUserLevel': '1000', 'UpgradeUserLevel': '1', 'OrderMoney': '1.1'}
    order['OrderId'] = orderId
    print dao.Insert(order)
    order['OrderState'] = 1
    print dao.Update(order)

    print dao.Query(order['OrderId'])
    print dao.QueryByUserId(order['UserId'])
    print dao.Delete(order['OrderId'])

