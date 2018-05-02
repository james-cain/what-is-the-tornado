#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class NoticeDao(base.DBBase):
    TableName = 'NoticeInfo'
    FieldNoticeNo = 'NoticeNo'

    def QueryNotice(self, noticeNo=None):
        sql = "select * from %s" % self.TableName
        if noticeNo:
            sql += " where %s = %s " %s (self.FieldNoticeNo, noticeNo)
        ret = self.ExecuteResult(sql)
        return ret

if __name__ == '__main__':
    dao = NoticeDao()
    print dao.QueryNotice()
