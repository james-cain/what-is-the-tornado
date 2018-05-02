#encoding=utf-8
import tornado.web
import urllib2
import urllib
import json
import base
import random
import hashlib

# local module
from utils.log import logger

class SendsmsHandler(base.BaseHandler):
    uid = "104494"
    #pwd = "5UrlGU"
    url = "http://119.23.114.82:6666/cmppweb/sendsms"
    pwd = "9b07b9a100186a296309ce4c160ccb95"
    srcphone = '106910134494'
    msg_prefix = '【快讯通】您的验证码为：'

    # to generate md5 str, and compare {"code": 529119, "userId": "myb123456789"}
    def post(self):
        self.set_header('Content-Type', 'application/json')
        ret = {'code': 0, 'msg': '', 'data': ''}
        userId = self.current_user
        if not userId:
            ret['code'] = 1
            ret['msg'] = 'forbidden'
            self.write(json.dumps(ret))
            self.finish()
            return
        mobile = self.get_argument('mobile', default=None)
        if not mobile:
            ret['code'] = 2
            ret['msg'] = 'params error'
            self.write(json.dumps(ret))
            self.finish()
            return
        code = random.randint(100000, 999999)

        data = {
            "uid": self.uid,
            "pwd": self.pwd,
            "srcphone": self.srcphone,
            "mobile": mobile,
            "msg": self.msg_prefix + str(code)
        }

        print code
        #response = urllib2.urlopen(self.url, urllib.urlencode(data))
        #ret_data = response.read()
        #if ret_data.startswith('0,'):
            # send success.
        rdata = '%s%s' % (userId,code)
        print rdata
        md5 = hashlib.md5()
        md5.update(rdata)
        ret['data'] = md5.hexdigest()
        print ret['data']
        self.write(json.dumps(ret))
        self.finish()
        return
        #else:
        #    ret['code'] = 3
        #    ret['msg'] = 'send sms failed'
        #    self.write(json.dumps(ret))
        #    self.finish()
        #    return
