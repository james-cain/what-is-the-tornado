#encoding=utf-8
import tornado.web
import urllib2
import json

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler

#GET     # Read  
#POST    # Create  
#PUT     # Update  
#DELETE  # Delete

# /api/user/json/{userid}, default is current user

class UserResource(RestHandler):
    DefaultParent = {
        daos.userDao.FieldUserName: '91卡哥',
        daos.userDao.FieldUserPhone: '05918899001',
        daos.userDao.FieldUserWeChatId: 'gh_974eb3e26735',
        daos.userDao.FieldUserPosterUrl: '/static/images/91kage.jpg',
        daos.userDao.FieldUserNo: '0',
    }
    # get 方法使用 authenticated会跳转登录页。这里我们自己判断.
    # 参考 tornado web.py -- def authenticated(method):
    #@tornado.web.authenticated
    @get(_path="/api/user/json/other/{userId}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def GetUser(self, userId):
        if not self.current_user:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        return {'userId':'123456', 'name':'3241'}

    @get(_path="/api/user/json/parent", _produces=mediatypes.APPLICATION_JSON)
    def GetParentUser(self):
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        parentUser = daos.userDao.QueryParentUser(userId)
        if parentUser:
            user = {
                daos.userDao.FieldUserName: parentUser[daos.userDao.FieldUserName],
                daos.userDao.FieldUserPhone: parentUser[daos.userDao.FieldUserPhone],
                daos.userDao.FieldUserWeChatId: parentUser[daos.userDao.FieldUserWeChatId],
                daos.userDao.FieldUserPosterUrl: parentUser[daos.userDao.FieldUserPosterUrl],
                daos.userDao.FieldUserNo: parentUser[daos.userDao.FieldUserNo],
            }
            return {'code': 0, 'msg': '', 'data': user}
        else:
            return {'code': 0, 'msg': '', 'data': self.DefaultParent}

    @get(_path="/api/user/json/childrenrank", _produces=mediatypes.APPLICATION_JSON)
    def GetChildUserRank(self):
        #userId = 'de11428635cd11e8afc500163e0309bf'
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        childUser = daos.userDao.QueryChildUser(userId)
        # 对于每个下级用户，查询下级用户的客户数
        childUserArr = []
        if childUser:
            for u in childUser:
                user = daos.userDao.QueryChildUser(u[daos.userDao.FieldUserId])
                if user: 
                    count = len(user)
                else:
                    count = 0
                childUserArr.append({
                    daos.userDao.FieldUserAddTime: u[daos.userDao.FieldUserAddTime],
                    daos.userDao.FieldUserName: u[daos.userDao.FieldUserName],
                    daos.userDao.FieldUserPhone: u[daos.userDao.FieldUserPhone],
                    daos.userDao.FieldUserWeChatId: u[daos.userDao.FieldUserWeChatId],
                    daos.userDao.FieldUserLevel: u[daos.userDao.FieldUserLevel],
                    daos.userDao.FieldUserPosterUrl: u[daos.userDao.FieldUserPosterUrl],
                    daos.userDao.FieldUserNo: u[daos.userDao.FieldUserNo],
                    'ChildAmount': count
                })
        return {'code': 0, 'msg': '', 'data': childUserArr}

    @get(_path="/api/user/json/children", _produces=mediatypes.APPLICATION_JSON)
    def GetChildUser(self):
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret

        childUser = daos.userDao.QueryChildUser(userId)
        grandChildUser = daos.userDao.QueryGrandChildUser(userId)
        childUserArr = []
        grandChildUserArr = []
        if childUser:
            for u in childUser:
                childUserArr.append({
                    daos.userDao.FieldUserAddTime: u[daos.userDao.FieldUserAddTime],
                    daos.userDao.FieldUserName: u[daos.userDao.FieldUserName],
                    daos.userDao.FieldUserPhone: u[daos.userDao.FieldUserPhone],
                    daos.userDao.FieldUserWeChatId: u[daos.userDao.FieldUserWeChatId],
                    daos.userDao.FieldUserLevel: u[daos.userDao.FieldUserLevel],
                    daos.userDao.FieldUserPosterUrl: u[daos.userDao.FieldUserPosterUrl],
                    daos.userDao.FieldUserNo: u[daos.userDao.FieldUserNo],
                })
        if grandChildUser:
            for u in grandChildUser:
                grandChildUserArr.append({
                    daos.userDao.FieldUserAddTime: u[daos.userDao.FieldUserAddTime],
                    daos.userDao.FieldUserName: u[daos.userDao.FieldUserName],
                    daos.userDao.FieldUserPhone: u[daos.userDao.FieldUserPhone],
                    daos.userDao.FieldUserWeChatId: u[daos.userDao.FieldUserWeChatId],
                    daos.userDao.FieldUserLevel: u[daos.userDao.FieldUserLevel],
                    daos.userDao.FieldUserPosterUrl: u[daos.userDao.FieldUserPosterUrl],
                    daos.userDao.FieldUserNo: u[daos.userDao.FieldUserNo],
                })

        return {'code': 0, 'msg': '', 'data': {'child': childUserArr, 'grandChild': grandChildUserArr}}

    @get(_path="/api/user/json/current", _produces=mediatypes.APPLICATION_JSON)
    def GetCurrentUser(self):
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        user = daos.userDao.QueryUser(userId)
        if not user:
            ret = {'code': 1, 'msg': 'no user', 'data': ''}
        else:
            ret = {'code': 0, 'msg': '', 'data': user}
        return ret

    @put(_path='/api/user/json/current',
	_types=[str],
        _consumes=mediatypes.APPLICATION_JSON,
        _produces=mediatypes.APPLICATION_JSON)
    def UpdateCurrentUser(self, user):
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        user['UserId'] = userId
        ret = daos.userDao.UpdateUser(user)
        if ret:
            return {'code': 0, 'msg': 'success', 'data': ''}
        else:
            return {'code': 0, 'msg': 'failed to update, see server log', 'data': ''}
