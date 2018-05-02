#encoding=utf-8

from user_resource import UserResource
from bank_resource import BankResource
from wxjsapi_resource import WeChatJsApiResource
from creditcard_orders_resource import CreditCardOrdersResource
from notice_resource import NoticeResource
from user_upgrade_resource import UserUpgradeResource
from user_level_resource import UserLevelResource

ResourceHandlers = [
    UserResource,
    BankResource,
    WeChatJsApiResource,
    CreditCardOrdersResource,
    NoticeResource,
    UserUpgradeResource,
    UserLevelResource,
]
