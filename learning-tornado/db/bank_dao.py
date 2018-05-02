#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class BankDao(base.DBBase):
    BankTableName = 'BankInfo'
    FieldBankNo = 'BankNo'

    def QueryBank(self, bankNo=None):
        sql = "select * from %s" % self.BankTableName
        if bankNo:
            sql += " where %s = %s " %s (self.FieldBankNo, bankNo)
        ret = self.ExecuteResult(sql)
        return ret

if __name__ == '__main__':
    dao = BankDao()
    print dao.QueryBank()
