#encoding=utf-8
import urllib2
import json

# local module
from utils.log import logger
from wx_config import WxConfig

''' 使用授权也返回的code 来获取用户信息'''
def GetUserInfo(code):
    try:
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (WxConfig.AppID, WxConfig.AppSecret, code)
        response = urllib2.urlopen(token_url)
        data = response.read();

        token_data = json.loads(data)
        if (token_data.get('errcode')):
            return {'state': 1, 'errcode': token_data.get('errcode'), 'errmsg': token_data.get('errmsg')}

        userinfo_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (token_data['access_token'], token_data['openid'])
        userinfo = urllib2.urlopen(userinfo_url).read()

        if (token_data.get('errcode')):
            return {'state': 2, 'errcode': token_data.get('errcode'), 'errmsg': token_data.get('errmsg')}

        return {'state':0, 'userinfo':userinfo, 'token_data':json.dumps(token_data)}
        
    except Exception, e:
        logger.error('Get Wx user info error %s' % str(e))
        return {'state':3, 'errcode':0, 'errmsg':str(e)} 

def GetUserOauth(redirect_url, state):
    aouth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s&connect_redirect=1#wechat_redirect" % (WxConfig.AppID, redirect_url, state)
    return aouth_url
