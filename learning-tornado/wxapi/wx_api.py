#encoding=utf-8
import time
import random
import string

from redis import Redis
from wechatpy import WeChatClient
from wechatpy.session.redisstorage import RedisStorage
from wechatpy.client.api import WeChatJSAPI
from wechatpy.oauth import WeChatOAuth
from wechatpy.pay import WeChatPay

from wx_config import WxConfig
from utils.log import logger

redis_client = Redis.from_url('redis://127.0.0.1:6379/0')
session_interface = RedisStorage(
    redis_client,
    prefix="wechatpy"
)
wechat_client = WeChatClient(
    WxConfig.AppID,
    WxConfig.AppSecret,
    session=session_interface
)

wechat_jsapi = WeChatJSAPI(wechat_client)

def get_jsapi_signature(url):
    jsapi_ticket = wechat_jsapi.get_jsapi_ticket()
    ret = {
        'noncestr': __create_nonce_str(15),
        'jsapi_ticket': jsapi_ticket,
        'timestamp': __create_timestamp(),
        'url': url,
        'appid': WxConfig.AppID
    }
    try:
        ret['signature'] = wechat_jsapi.get_jsapi_signature(
            ret['noncestr'],
            ret['jsapi_ticket'],
            ret['timestamp'],
            url)
    except Exception, e:
        ret['signature'] = 'signature failed, see server log'
        logger.debug('signature failed %s' % str(e))
    return ret
def __create_nonce_str(r):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(r))

def __create_timestamp():
    return int(time.time())

def sendMessage(openId, text):
    try:
        ret = wechat_client.message.send_text(openId, text)
    except Exception, e:
        print e
        logger.debug('send message error %s %s %s' % (openId, text, str(e)))

if __name__ == '__main__':
    sendMessage('oMMOX1SXesai-Ibv3Za_nYIZmAoY', u'下级[童大宝。]升级会员啦, 收到分润[23880.0]分')
    #print wechat_client.access_token
    #print wechat_jsapi.get_jsapi_ticket()
