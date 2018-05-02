#encoding=utf-8
import tornado.web
import urllib2
import json

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler


class BankResource(RestHandler):
    @get(_path="/api/bank/json/{bankId}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def GetBank(self, bankId):
        if not self.current_user:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        return {'userId':'123456', 'name':'3241'}

    # return all banks..
    @get(_path="/api/bank/json/", _produces=mediatypes.APPLICATION_JSON)
    def GetBanks(self):
        if not self.current_user:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        ret = daos.bankDao.QueryBank()
        return {'code': 0, 'msg': 'success', 'data': ret}

