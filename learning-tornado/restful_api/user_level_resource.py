#encoding=utf-8
import tornado.web
import urllib2
import json

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler

class UserLevelResource(RestHandler):
    @get(_path="/api/userlevel/json/{level}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def GetBank(self, level):
        if not self.current_user:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        return {'level':'123456', 'name':'3241'}

    # return all levels
    @get(_path="/api/userlevel/json/", _produces=mediatypes.APPLICATION_JSON)
    def GetLevels(self):
        if not self.current_user:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        ret = daos.userLevelDao.Query()
        return {'code': 0, 'msg': 'success', 'data': ret}

