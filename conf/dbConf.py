#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/9/3 10:44
@Desc   ：封装获取数据库，方便使用

@使用：
# 代码上面添加
from conf.dbConf import db_user

db.db_name

=================================================='''
import yaml

from conf.logConf import logger


class GetDBYaml:
    def __init__(self, DIR_DB_yaml=r'./databases.yaml'):
        """

        :param DIR_DB_yaml: 数据库配置文件，如没填写则使用默认的
        """

        # 打开数据库配置yaml文件
        stream = open(DIR_DB_yaml, 'r', encoding='utf-8')
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

    def getUser(self):
        return self.user

    def getPassWord(self):
        return self.password

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def getCharset(self):
        return self.charset

    def getDBName(self):
        return self.db_name

    def getTableName(self):
        return self.table_name


db_user = GetDBYaml().getUser()
db_password = GetDBYaml().getPassWord()
db_host = GetDBYaml().getHost()
db_port = GetDBYaml().getPort()
db_charset = GetDBYaml().getCharset()
db_name = GetDBYaml().getDBName()
db_table_name = GetDBYaml().getTableName()

if __name__ == "__main__":
    # 对上面代码进行测试
    from conf.dbConf import db_user

    print(db_user)
    print(db_password)
    print(db_host)
    print(db_port)

    print(db_charset)
    print(db_name)
    print(db_table_name)

    # 导入日志系统测试
    logger.info('从其他地方导入打印日志看下')
