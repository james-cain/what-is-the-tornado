#encoding=utf-8
import tornado.web
import urllib2
import json
import hashlib

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler

from wxapi import wx_api

#GET     # Read  
#POST    # Create  
#PUT     # Update  
#DELETE  # Delete

class Signature(object):
    url = str

class WeChatJsApiResource(RestHandler):
    @post(_path="/api/wechat/jsapi/signature/json",
	_types=[Signature],
        _consumes=mediatypes.APPLICATION_JSON,
        _produces=mediatypes.APPLICATION_JSON)
    def PostSignature(self, signature):
        if not self.current_user:
            print 'signature failed not login'
            return {'code': 2, 'msg': 'permision denied', 'data': ''}

        print signature.url
        data = wx_api.get_jsapi_signature(signature.url)
        return {'code': 0, 'msg': '', 'data': data}
