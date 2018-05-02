/*
Navicat MySQL Data Transfer

Source Server         : 47.95.243.154_3306
Source Server Version : 50721
Source Host           : 47.95.243.154:3306
Source Database       : kageweb 

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-03-18 18:56:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for User
-- ----------------------------
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `UserId` varchar(255) NOT NULL,
  `UserName` varchar(255) DEFAULT '',
  `UserSex` int(1) DEFAULT '0',
  `UserPhone` varchar(255) DEFAULT '',
  `UserAddr` varchar(255) DEFAULT '',
  `UserShareBenefitMoney` float(10,0) DEFAULT '0',
  `UserRedPaperMoney` float(10,0) DEFAULT '0' COMMENT '红包分润',
  `UserPosterUrl` varchar(1024) DEFAULT '',
  `UserPassword` varchar(255) DEFAULT '' COMMENT '暂时用微信登录',
  `UserWeChatId` varchar(255) DEFAULT '',
  `UserArea` varchar(255) DEFAULT '',
  `UserNo` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户编号',
  `UserLevel` int(10) unsigned DEFAULT '1000',
  `UserIDCard` varchar(255) DEFAULT '' COMMENT '用户身份证号',
  `ParentId` varchar(255) CHARACTER SET latin1 DEFAULT '' COMMENT '上一级',
  `GrandParentId` varchar(255) DEFAULT '' COMMENT '上二级',
  `GreatGrandParentId` varchar(255) DEFAULT '' COMMENT '上三级',
  PRIMARY KEY (`UserNo`),
  UNIQUE KEY `UserId` (`UserId`) USING BTREE,
  KEY `UserLevel` (`UserLevel`),
  CONSTRAINT `UserLevel` FOREIGN KEY (`UserLevel`) REFERENCES `UserLevel` (`UserLevel`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for UserLevel
-- ----------------------------
DROP TABLE IF EXISTS `UserLevel`;
CREATE TABLE `UserLevel` (
  `UserLevel` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '用户等级',
  `ProfitShare` float NOT NULL COMMENT '用户等级对应的分配比例',
  `args1` varchar(255) DEFAULT NULL,
  `args2` varchar(255) DEFAULT NULL,
  `args3` varchar(255) DEFAULT NULL,
  KEY `UserLevel` (`UserLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for WeChat
-- ----------------------------
DROP TABLE IF EXISTS `WeChat`;
CREATE TABLE `WeChat` (
  `UserId` varchar(255) NOT NULL,
  `OpenId` varchar(255) NOT NULL COMMENT '微信对于公众号的OpenID',
  `AccessToken` varchar(255) NOT NULL,
  `RefreshToken` varchar(255) NOT NULL,
  `Scope` varchar(255) DEFAULT NULL,
  `ExpiresIn` int(11) NOT NULL,
  PRIMARY KEY (`OpenId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
