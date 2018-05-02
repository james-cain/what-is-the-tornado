#encoding=utf-8
import tornado.web
import urllib2
import json
import uuid
import time

# local module
from db import daos
from wxapi import wx_pay
from manager import managers

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler

from xml.dom import minidom

path = '/api/user/upgrade/wechatpay/action'
NotifyUrl = 'http://m.91kgxy.com/' + path
fail_xml = minidom.parseString('<xml><return_code><![CDATA[FAILED]]></return_code></xml>')
success_xml = minidom.parseString('<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>')

class UserUpgradeResource(RestHandler):
    @post(_path="/api/user/upgrade/wechatpay/json/",
	_types=[str],
        _consumes=mediatypes.APPLICATION_JSON,
        _produces=mediatypes.APPLICATION_JSON)
    def CreateOrder(self, order):
        userId = self.current_user
        if not userId:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        orderNo = ''.join(str(uuid.uuid1()).split('-'))
        order[daos.userUpgradeOrderDao.FieldUserId] = userId 
        order[daos.userUpgradeOrderDao.FieldOrderId] = orderNo
        order[daos.userUpgradeOrderDao.FieldAddTime] = int(time.time())
        order[daos.userUpgradeOrderDao.FieldModifyTime] = int(time.time())

        originLevel = order[daos.userUpgradeOrderDao.FieldOrigin]
        upgradeLevel = order[daos.userUpgradeOrderDao.FieldUpgrade]
        origin = daos.userLevelDao.Query(originLevel)
        upgrade = daos.userLevelDao.Query(upgradeLevel)
        #order['OrderMoney'] = int((upgrade[daos.userLevelDao.FieldMoney] - origin[daos.userLevelDao.FieldMoney]) * 100)
        order['OrderMoney'] = int(upgrade[daos.userLevelDao.FieldMoney] * 100)

        openId = daos.userDao.QueryWeChatOpenId(userId)
        if not openId:
            return {'code': 3, 'msg': 'no open id', 'data': ''}
        detail = u'会员升级[%s-%s]' % (order['OriginUserLevel'], order['UpgradeUserLevel'])
        # 统一下单接口
        params = wx_pay.CreateWeChatOrder(
            NotifyUrl,
            order['OrderMoney'],
            self.request.remote_ip,
            openId,
            orderNo, # 系统订单号，和微信订单号一致
            detail)
        if params:
            # 生成系统后台订单
            ret = daos.userUpgradeOrderDao.Insert(order)
            params['orderId'] = orderNo # 返回OrderId 供后续查询

            if ret:
                return {'code': 0, 'msg': 'success', 'data': params}
            else:
                return {'code': 1, 'msg': 'failed, see server log', 'data': ''}

    @post(_path=path,
        _types=[str],
        _consumes=mediatypes.TEXT_XML, # 这里直接传入body内容，自己修改的
        _produces=mediatypes.APPLICATION_XML)
    def WeChatPayNotify(self, notify_xml):
        # 解析返回值，验证签名
        try:
            notify = wx_pay.ParsePaymentResult(notify_xml)
        except Exception, e:
            return fail_xml
        # 验证状态，金额
        if notify['return_code'] == 'SUCCESS':
            total_fee = notify['total_fee']
            orderId = notify['out_trade_no']
            # check order state.
            # check total_fee.
            order = daos.userUpgradeOrderDao.Query(orderId)
            if not order:
                return fail_xml
            if order[daos.userUpgradeOrderDao.FieldOrderState] == 0:
                # 已支付 更新支付状态
                order[daos.userUpgradeOrderDao.FieldOrderState] = 1
                # 更新修改时间
                order[daos.userUpgradeOrderDao.FieldModifyTime] = int(time.time())
                # 验证金额是否相等。。。
                if int(order[daos.userUpgradeOrderDao.FieldMoney]) != total_fee:
                    return fail_xml
                # 更新订单
                if daos.userUpgradeOrderDao.Update(order):
                    # 处理支付后续逻辑
                    managers.userManager.UserUpgrade(
                        order[daos.userUpgradeOrderDao.FieldUserId],
                        order[daos.userUpgradeOrderDao.FieldOrigin],
                        order[daos.userUpgradeOrderDao.FieldUpgrade],
                        order[daos.userUpgradeOrderDao.FieldMoney])
                    return success_xml
        else:
            print notify['return_msg']
            return fail_xml

    @get(_path="/api/user/upgrade/wechatpay/{orderId}",
        _types=[str],
        _produces=mediatypes.APPLICATION_JSON)
    def GetUpgradeOrder(self, orderId):
        userId = self.current_user
        if not userId:
            return {'code': 2, 'msg': 'permision denied', 'data': ''}
        ret = daos.userUpgradeOrderDao.Query(oderId)
        if ret:
            return {'code': 2, 'msg': 'permision denied', 'data': ret}
        return {'code': 2, 'msg': 'query error, see server log', 'data': ''}
