#encoding=utf-8

from db import daos
from wxapi import wx_api

upgrade_profit_parent = 0.6
upgrade_profit_grandparent = 0.3

class UserManager:
    def __init__(self, logger=None):
        self.logger = logger
    # 用户升级成功
    def UserUpgrade(self, userId, originLevel, upgradeLevel, money):
        # update user level.
        user = daos.userDao.QueryUser(userId)
        user[daos.userDao.FieldUserLevel] = upgradeLevel

        parentId = user[daos.userDao.FieldParentId]
        grandParentId = user[daos.userDao.FieldGrandParentId]

        # 更新用户等级
        ret = daos.userDao.UpdateUser(user)
        if not ret:
            return

        # 有上级用户 分配利润, 这里是否要生成 账目变化记录
        if parentId:
            self.UpdateUserMoney(user, parentId, money * upgrade_profit_parent)
            if grandParentId:
                self.UpdateUserMoney(user, grandParentId, money * upgrade_profit_grandparent)

    def UpdateUserMoney(self, upgradeUser, userId, money):
        msg = u'下级[%s]升级会员啦, 收到分润[%s]分' % (upgradeUser['UserName'], money)
        self.NotifyUser(upgradeUser, userId, msg)
        ret = daos.userDao.AddUserShareBenefitMoney(userId, money)
        if ret:
            # 生成账变记录
            daos.userMoneyRecordDao.Insert(userId, 0, money, msg)
        return ret

    def NotifyUser(self, upgradeUser, notify_user_id, msg):
        # 通知用户
        openId = daos.userDao.QueryWeChatOpenId(notify_user_id)
        wx_api.sendMessage(openId, msg)
        return

if __name__ == '__main__':
    manager = UserManager()
    #userId = 'a55dd856367b11e8afc500163e0309bf'
    #upgradeLevel = '3'
    #money = 100
    #manager.UserUpgrade(userId, 1000, upgradeLevel, money)
    #manager.NotifyUser(None, 'de11428635cd11e8afc500163e0309bf', '和哈哈哈哈') 
