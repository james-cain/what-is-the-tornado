#encoding=utf-8
import tornado.web
import urllib2
import json

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler


class NoticeResource(RestHandler):

    # return all banks..
    @get(_path="/api/notice/json/", _produces=mediatypes.APPLICATION_JSON)
    def GetNotices(self):
        if not self.current_user:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        ret = daos.noticeDao.QueryNotice()
        return {'code': 0, 'msg': 'success', 'data': ret}

