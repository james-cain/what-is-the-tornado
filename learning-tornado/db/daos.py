import user_dao
import bank_dao
import credit_card_orders_dao
import notice_dao
import user_upgrade_order_dao
import user_level_dao
import user_money_record_dao

from utils.log import logger

userDao = user_dao.UserDao(logger)
bankDao = bank_dao.BankDao(logger)
noticeDao = notice_dao.NoticeDao(logger)
creditCardOrdersDao = credit_card_orders_dao.CreditCardOrdersDao(logger)
userUpgradeOrderDao = user_upgrade_order_dao.UserUpgradeOrderDao(logger)
userLevelDao = user_level_dao.UserLevelDao(logger)
userMoneyRecordDao = user_money_record_dao.UserMoneyRecordDao(logger)
