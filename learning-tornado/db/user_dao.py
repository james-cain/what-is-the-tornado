#encoding=utf-8
import uuid
import time
import base
import MySQLdb

class UserDao(base.DBBase):
    # UserTableName = 'User'
    # WeChatTableName = 'WeChat'
    # FieldOpenId = 'OpenId'
    # FieldUserId = 'UserId'
    # FieldUserNo = 'UserNo'
    # FieldUserPhone = 'UserPhone'
    # FieldUserName = 'UserName'
    # FieldUserPosterUrl = 'UserPosterUrl'
    # FieldUserWeChatId = 'UserWeChatId'
    # FieldParentId = 'ParentId'
    # FieldGrandParentId = 'GrandParentId'
    # FieldGreatGrandParentId = 'GreatGrandParentId'
    # FieldUserLevel = 'UserLevel'
    # FieldUserMoney = 'UserShareBenefitMoney'
    # FieldUserTotalMoney = 'UserTotalBenefit'
    # FieldUserAddTime = 'UserAddTime'
    UserTableName = 'UserTable'
    FieldUserId = 'UserId'
    FieldUserAvatar = 'UserAvatar'
    FieldUserName = 'UserName'
    FieldUserQrcode = 'UserQrcode'
    FieldUserCompany = 'UserCompany'
    FieldUserDuty = 'UserDuty'
    FieldUserArea = 'UserArea'
    FieldUserLive = 'UserLive'
    FieldUserProfession = 'UserProfession'
    FieldUserPhone = 'UserPhone'
    FieldUserAddress = 'UserAddress'
    FieldUserHobby = 'UserHobby'
    FieldUserExperience = 'UserExperience'
    FieldUserDepartment = 'UserDepartment'
    FieldUserDeptIntroduce = 'UserDeptIntroduce'
    FieldUserEnterprise = 'UserEnterprise'
    FieldUserContribute = 'UserContribute' 


    def AddUserShareBenefitMoney(self, userId, money):
        sql = "update %s set %s = %s + %s, %s = %s + %s where %s = '%s'" % (
            self.UserTableName,
            self.FieldUserMoney,
            self.FieldUserMoney,
            money,
            self.FieldUserTotalMoney,
            self.FieldUserTotalMoney,
            money,
            self.FieldUserId, userId)
        return self.Execute(sql)

    def InsertUser(self, user):
        user[self.FieldUserAddTime] = int(time.time())
        qmarks = ', '.join(['%s'] * len(user)) # 用于替换记录值
        cols = ', '.join(user.keys()) # 字段名
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.UserTableName, cols, qmarks)
        return self.Execute(sql, user.values())

    def QueryWeChat(self, openId):
        sql = "select * from %s where %s = '%s'" % (self.WeChatTableName, self.FieldOpenId, openId)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret[0]['UserId']
        return None 

    def QueryWeChatOpenId(self, userId):
        sql = "select * from %s where %s='%s'" % (self.WeChatTableName, self.FieldUserId, userId)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret[0]['OpenId']
        return None 

    def InsertWeChat(self, data):
        qmarks = ', '.join(['%s'] * len(data)) # 用于替换记录值
        cols = ', '.join(data.keys()) # 字段名
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.WeChatTableName, cols, qmarks)
        return self.Execute(sql, data.values())

    def QueryUser(self, userId):
        sql = "select * from %s where %s = '%s'" % (self.UserTableName, self.FieldUserId, userId)
        ret = self.ExecuteResult(sql)
        if ret:
            return ret[0]

    def QueryUserInfo(self):
        sql = "select * from %s" % (self.UserTableName)
        ret = self.ExecuteResult(sql)
        if ret:
            return ret

    def QueryParentUser(self, userId):
        sql = "select * from %s where %s = '%s'" % (self.UserTableName, self.FieldUserId, userId)
        ret = self.ExecuteResult(sql)
        if ret and ret[0][self.FieldParentId]:
            sql = "select * from %s where %s = '%s'" % (self.UserTableName, self.FieldUserId, ret[0][self.FieldParentId])
            ret = self.ExecuteResult(sql)
            if ret:
                return ret[0]

    def QueryChildUser(self, userId):
        sql = "select * from %s where %s = '%s'" % (self.UserTableName, self.FieldParentId, userId)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret
        return None

    def QueryGrandChildUser(self, userId):
        sql = "select * from %s where %s = '%s'" % (self.UserTableName, self.FieldGrandParentId, userId)
        ret = self.ExecuteResult(sql)
        if ret and len(ret) > 0:
            return ret
        return None

    def UpdateUser(self, user):
        fields = []
        # update except id and no.
        for key in user.keys():
            if key != self.FieldUserId and key != self.FieldUserNo:
                fields.append("%s='%s'" % (key, user[key]))
        fields = ', '.join(fields) # 字段名
        where = "%s='%s'" % (self.FieldUserId, user[self.FieldUserId])
        sql = "UPDATE %s SET %s where %s" % (self.UserTableName, fields, where)
        return self.Execute(sql)

    def DeleteUser(self, user):
        return

    def GetParentUser(self, userId):
        if userId == None or userId == '':
            return None
        parentUser = self.QueryUser(userId)
        return parentUser

    def GenerateUserByWeChat(self, userInfo, tokenInfo, parentId=None):

        userId = ''.join(str(uuid.uuid1()).split('-'))
        user = {'UserId': userId, 'UserName':userInfo['nickname'], 'UserSex':userInfo['sex'], 'UserArea':userInfo['city'], 'UserPosterUrl': userInfo['headimgurl']}

        parentUser = self.GetParentUser(parentId)
        # 有上级用户
        if parentUser:
            user[self.FieldParentId] = parentUser[self.FieldUserId]
            user[self.FieldGrandParentId] = parentUser[self.FieldParentId]
            user[self.FieldGreatGrandParentId] = parentUser[self.FieldGrandParentId]

        if self.InsertUser(user):
            t = int(time.time()) + tokenInfo['expires_in']
            data = {'UserId': userId, 'OpenId': tokenInfo['openid'], 'AccessToken': tokenInfo['access_token'], 'RefreshToken': tokenInfo['refresh_token'], 'Scope': tokenInfo['scope'], 'ExpiresIn':t}
            if self.InsertWeChat(data):
                return userId
        return None
def UpdateMoneyTest():
    userDao = UserDao()
    userDao.AddUserShareBenefitMoney('4caaf29c35c811e8afc500163e0309bf', 100)

def UpdateUserTest():
    userDao = UserDao()
    user = userDao.QueryUser('8aa3ef66-2ad0-11e8-afc5-00163e0309bf')
    userUpdate = {'UserId': user['UserId'], 'UserPhone': '12345678543', 'UserAddr': '12312321312312'}
    userDao.UpdateUser(userUpdate)

def WeChatTest():
    tokenInfo = {
        "access_token":"ACCESS_TOKEN",
        "expires_in":7200,
        "refresh_token":"REFRESH_TOKEN",
        "openid":"OPENID-1",
        "scope":"SCOPE"
    }
    userInfo = {
        "openid": "OPENID-1",
        "nickname": 'hhh',
        "sex": "1",
        "province": "PROVINCE",
        "city": "CITY",
        "country": "COUNTRY",
        "headimgurl": "",
        "privilege": [ "PRIVILEGE1" "PRIVILEGE2" ],
        "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }

    userDao = UserDao()
    # 添加用户 Openid-1
    uid1 = userDao.GenerateUserByWeChat(userInfo, tokenInfo)

    # 添加用户 Openid-2
    userInfo['openid'] = 'OPENID-2'
    tokenInfo['openid'] = 'OPENID-2'
    uid2 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId=uid1)

    # 添加用户 Openid-3
    userInfo['openid'] = 'OPENID-3'
    tokenInfo['openid'] = 'OPENID-3'
    uid3 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId=uid1)

    # 添加用户 Openid-4
    userInfo['openid'] = 'OPENID-4'
    tokenInfo['openid'] = 'OPENID-4'
    uid4 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid3)

    # 添加用户 Openid-5
    userInfo['openid'] = 'OPENID-5'
    tokenInfo['openid'] = 'OPENID-5'
    uid5 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid2)

    # 添加用户 Openid-6
    userInfo['openid'] = 'OPENID-6'
    tokenInfo['openid'] = 'OPENID-6'
    uid6 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid4)

    # 添加用户 Openid-7
    userInfo['openid'] = 'OPENID-7'
    tokenInfo['openid'] = 'OPENID-7'
    uid7 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid6)

if __name__ == '__main__':
    print UpdateMoneyTest()
