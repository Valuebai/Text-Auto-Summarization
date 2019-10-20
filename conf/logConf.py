#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/9/3 10:44
@Desc   ：封装log日志，方便使用

注意：flask 有自带的log，导入自创建的文件后会覆盖flask自带的

# 将logging.ini文件用python代码写出来

@使用：
# 代码上面添加
from conf.logConf import logger

# 在具体需要的地方
logger.info('开始连接数据库...')
logger.error(e)
=================================================='''

import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import os
import time

# from conf.dbConf import db_user, db_charset, db_host, db_name, db_password, db_port, db_table_name


class GetLogger:

    def __init__(self, DIR_logs=r'./logs', setLogLevel=logging.INFO):
        """
        获取日志信息
        :param DIR_logs: 存放日志文件夹logs，如没填写则使用默认的
        """

        # 实例化root日志对象
        self.logger = logging.getLogger('root')

        # 设置日志的输出级别
        self.logger.setLevel(setLogLevel)

        # 如果logs文件夹不存在，则创建
        if not os.path.exists(DIR_logs):
            os.mkdir(DIR_logs)

        # 获取今天的日期
        getTodayDateStr = time.strftime("%Y-%m-%d", time.localtime(time.time()))

        # 定义日志的输出格式
        log_formatter = logging.Formatter(
            "[%(asctime)s][%(pathname)s: line(%(lineno)d)][%(levelname)s][thread:%(thread)d] - %(message)s")

        # 定义日志的处理/存储方式
        fh = TimedRotatingFileHandler(
            filename=DIR_logs + r'/' + getTodayDateStr + r".log",  # 定义日志的存储
            when="MIDNIGHT",  # 按照日期进行切分when = D： 表示按天进行切分,or self.when == 'MIDNIGHT'
            interval=1,  # interval = 1： 每天都切分。 比如interval = 2就表示两天切分一下。
            backupCount=30,  # 保留30天的日志
            encoding="UTF-8",  # 使用UTF - 8的编码来写日志
            delay=False,
            utc=True  # utc = True: 使用UTC + 0的时间来记录 （一般docker镜像默认也是UTC + 0）
        )
        fh.setLevel(logging.DEBUG)  # 设置日志级别
        fh.setFormatter(log_formatter)  # 设置日志格式

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)  # 设置日志级别
        ch.setFormatter(log_formatter)  # 设置日志格式

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


logger = GetLogger().getlog()

if __name__ == "__main__":
    # 对上面代码进行测试
    logger = GetLogger().getlog()

    # 在具体需要的地方
    logger.info('INFO日志打印...')
    logger.error('ERROR日志打印...')

    ##导入数据库测试
    # print(db_user)
    # print(db_password)
    # print(db_host)
    # print(db_port)
    #
    # print(db_charset)
    # print(db_name)
    # print(db_table_name)
