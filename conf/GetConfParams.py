#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/9/3 10:44
@Desc   ：封装conf中的参数，方便使用

注意：flask 有自带的log，导入自创建的文件后会覆盖flask自带的

使用：
# 代码上面添加
from conf.GetConfParams import GetConfParams
logger = GetConfParams().logger

# 在具体需要的地方
logger.info('开始连接数据库...')
logger.error(e)
=================================================='''

import logging
import logging.config
import os
import yaml


class GetConfParams:
    # 如果上一级的log文件夹不存在，则创建
    if not os.path.exists('../log'):
        os.mkdir('../log')

    # 这里填下同一文件夹下的.ini文件
    log_path = os.path.join(os.path.dirname(__file__) + '/logging.ini')
    logging.config.fileConfig(log_path)

    def __init__(self):
        # 设置日志
        self.logger = logging.getLogger('root')

        # 这里填下同一文件夹下的.yaml文件
        yaml_path = os.path.join(os.path.dirname(__file__) + '/databases.yaml')

        # 打开yaml文件，如果没用到，可以注释掉下面的代码
        stream = open(yaml_path, 'r', encoding='utf-8')
        params = yaml.load(stream, Loader=yaml.FullLoader)

        # 设置数据库的连接地址、端口号、数据库名、用户名、密码
        self.user = params['database_conf']['user']
        self.password = params['database_conf']['password']
        self.host = params['database_conf']['host']
        self.port = params['database_conf']['port']

        # 设置charset为中文，有时候读取到的数据是乱码
        self.charset = params['database_conf']['charset']

        # 连接的数据库
        self.db_name = params['database_conf']['db_name']
        # 连接的表
        self.table_name = params['database_conf']['table_name']


if __name__ == "__main__":
    # 对上面代码进行测试
    get_db = GetConfParams()
    print(get_db.user)
    print(get_db.password)
    print(get_db.host)
    print(get_db.port)
    print(get_db.user)
    print(get_db.charset)
    print(get_db.db_name)
    print(get_db.table_name)

    logger = GetConfParams().logger

    # 在具体需要的地方
    logger.info('开始连接数据库...')
    logger.error('错误测试')
