#encoding=utf-8
import time
import random
import string
import json

from wechatpy.pay import WeChatPay
from wechatpy.pay.api import WeChatOrder
from wechatpy.pay.api import WeChatJSAPI

from wx_config import WxConfig
from wx_api import wechat_client
from utils.log import logger

weChatPay = WeChatPay(
    WxConfig.AppID,
    WxConfig.ApiKey,
    WxConfig.MchId,
    sub_mch_id = None,
    mch_cert = WxConfig.MchCert,
    mch_key = WxConfig.MchKey,
    timeout = 10,
)

weChatOrder = WeChatOrder(weChatPay)
weChatJSAPI = WeChatJSAPI(weChatPay)
notify_url = 'http://m.91kage.com/pay/create/result'
# 统一下单接口
def CreateWeChatOrder(notifyUrl, totalFee, clientIp, openId, orderId, detail):
    attach = json.dumps({'openId': openId, 'orderId':orderId})
    ret = weChatOrder.create(
        'JSAPI', # trade_type
        u'91卡哥金服-会员充值', # body
        totalFee, # total_fee 1块钱，单位分
        notifyUrl,  # notify_url
        client_ip = clientIp, # h5的IP
        user_id = openId, # openId
        out_trade_no = orderId,
        detail = detail, #商品详情,此处添加升级信息
        attach = json.dumps(attach), # 保留我们系统的order，以便查询
        device_info = 'WEB')

    if ret['return_code'] == 'SUCCESS':
        if ret['result_code'] == 'SUCCESS':
            params = weChatJSAPI.get_jsapi_params(ret['prepay_id'])
            return params
        else:
            logger.debug('create wechat order failed %s' % ret['err_code'])
            return None
    else:
        logger.debug('create wechat order failed %s' % ret['return_msg']) 
        return None

def ParsePaymentResult(xml):
    return weChatPay.parse_payment_result(xml)

if __name__ == '__main__': 
    clientIp = '119.29.135.61'
    openId = 'oMMOX1SXesai-Ibv3Za_nYIZmAoY'
    orderId = '12345678912345678912345678912346'
    detail = 'test'
    CreateWeChatOrder(notify_url, '100', clientIp, openId, orderId, detail)
