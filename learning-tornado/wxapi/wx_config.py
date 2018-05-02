#encoding=utf-8

class WxConfig(object):
    AppID = 'wx9253fa1ffd8dc814'  # AppID(应用ID)
    AppSecret = 'f86b9309c228912f4503bb0d2e778d02'  # AppSecret(应用密钥)
    ApiKey = 'fylb1234567890fylb1234567890fylb' #
    MchId = '1500322622' # 商户 id
    MchCert = None # 商户证书路径
    MchKey = None # 商户证书私钥路径

    # JSAPI 支付授权目录
    JSAPI_PAY_DIR = 'http://m.91kgxy.com/pay/wechat/'
    # 扫码支付 回调连接
    SCAN_PAY_CALLBACK_URL = 'http://m.91kgxy.com/pay/wechat/scan-pay-callback/'
    # H5支付域名
    H5_PAY_HOST = 'm.91kgxy.com'

    '''获取access_token'''
    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)
