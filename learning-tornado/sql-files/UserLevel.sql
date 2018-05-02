/*
Navicat MySQL Data Transfer

Source Server         : 47.95.243.154_3306
Source Server Version : 50721
Source Host           : 47.95.243.154:3306
Source Database       : 91Kage

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-03-19 00:36:44
*/

SET FOREIGN_KEY_CHECKS=0;

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
-- Records of UserLevel
-- ----------------------------
INSERT INTO `UserLevel` VALUES ('0', '0.2', '总代', null, null);
INSERT INTO `UserLevel` VALUES ('1', '0.18', '一级代理', null, null);
INSERT INTO `UserLevel` VALUES ('2', '0.16', '二级代理', null, null);
INSERT INTO `UserLevel` VALUES ('3', '0.14', '三级代理', null, null);
INSERT INTO `UserLevel` VALUES ('1000', '0', '普通会员', null, null);
