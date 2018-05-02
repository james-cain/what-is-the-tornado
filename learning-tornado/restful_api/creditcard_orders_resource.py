#encoding=utf-8
import tornado.web
import urllib2
import json
import uuid
import time

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler

# 申请信用卡订单

class CreditCardOrdersResource(RestHandler):

    # return all.
    @get(_path="/api/creditcardorders/json/", _produces=mediatypes.APPLICATION_JSON)
    def GetOrders(self):
        userId = self.current_user
        if not self.current_user:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        ret = daos.creditCardOrdersDao.QueryByUserId(userId)

        return {'code': 0, 'msg': '', 'data': ret}

    @post(_path="/api/creditcardorders/json/",
	_types=[str],
        _consumes=mediatypes.APPLICATION_JSON,
        _produces=mediatypes.APPLICATION_JSON)
    def CreateOrder(self, order):
        if not self.current_user:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        # 生成唯一订单号
        orderNo = ''.join(str(uuid.uuid1()).split('-'))
        order[daos.creditCardOrdersDao.FieldOrderNo] = orderNo
        order[daos.creditCardOrdersDao.FieldApplyTime] = int(time.time())

        ret = daos.creditCardOrdersDao.Insert(order)
        if ret:
            return {'code': 0, 'msg': 'success', 'data': 'orderNo'}
        else:
            return {'code': 1, 'msg': 'failed, see server log', 'data': ''}

    @delete(_path="/api/creditcardorders/json/{orderNo}",
	_types=[str],
        _produces=mediatypes.APPLICATION_JSON)
    def DeleteOrder(self, orderNo):
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
        ret = daos.creditCardOrdersDao.delete(orderNo)
        if ret:
            return {'code': 0, 'msg': 'success', 'data': 'orderNo'}
        else:
            return {'code': 1, 'msg': 'failed, see server log', 'data': ''}

if __name__ == '__main__':
    resource = CreditCardOrdersResource(None)
    order = {"UserId":"8aa3ef66-2ad0-11e8-afc5-00163e0309bf", "ApplyUserName":"123", "ApplyUserPhone": "234", "ApplyUserIDCard": "fdsfds", "ApplyBankNo": "1"}
    resource.CreateOrder(order)
