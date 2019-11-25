#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：Valuebai
@Date   ：2019/11/25 11:15
@Desc   ：

注意点：
1、Pycharm 默认使用unittest框架，设置pytest框架路径：
File->setting->Tools->Python Intergrated Tools->Default test runner->

【参考链接】https://blog.csdn.net/zha6476003/article/details/80646212

2、在使用pytest的固件（Fixture）时，可将固件函数写在conftest.py中，然后在test_xxx中具体的测试
不要自己显式调用 conftest.py，pytest 会自动调用，可以把 conftest 当做插件来理解。
=================================================='''
import pytest
import time

from APP.TextSummarization.textrank.textrank4zh_run import get_textrank4zh_keywords


# 测试获取的关键词不为空
@pytest.mark.parametrize("text", ["""生成摘要的主要思想是找到包含整个数据集“信息”的数据子集。这种技术在当今行业内被广泛使用。搜索引擎就是一个例子; 
        其他还包括文档摘要生成，图像收集和视频处理。文档摘要生成算法试图通过查找信息量最大的句子来创建整个文档的代表性摘要，而在图像摘要中，
        计算机则试图找到最具代表性的显著的图像。对于监控视频，人们可能希望从平静的环境影像中提取出重要事件。"""])
def test_get_textrank4zh_keywords(text):
    keyWords = get_textrank4zh_keywords(text)
    print('获取关键词：', keyWords)
    assert keyWords[0] != None


# pytest的使用说明
# ==================================================

# assert断言判断
def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


@pytest.mark.finished
def test_func1():
    assert 1 == 1


# 使用unfinished标记未完成的函数，得用下面的命令调用
# pytest -m finished tests/test_textSummarization.py
@pytest.mark.unfinished
def test_func2():
    assert 1 != 1


# 忽略跳过测试
@pytest.mark.skip(reason='out-of-date api')
def test_connect():
    pass


# 单个参数测试
# 执行命令：pytest -v tests/test_textSummarization.py::test_passwd_length
@pytest.mark.parametrize('passwd',
                         ['1234569',
                          'abcdefdfss',
                          'as52345fasdf4'])
def test_passwd_length(passwd):
    assert len(passwd) >= 8


# 多参数的例子，用于校验用户密码
# 执行命令：pytest -v tests/test_textSummarization.py::test_passwd_md5
@pytest.mark.parametrize('user, passwd', [('jack', 'abcdefgh'), ('tom', 'a123456a')])
def test_passwd_md5(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }

    import hashlib

    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]


'''
什么是固件
固件（Fixture）是一些函数，pytest 会在执行测试函数之前（或之后）加载运行它们。

我们可以利用固件做任何事情，其中最常见的可能就是数据库的初始连接和最后关闭操作。

Pytest 使用 pytest.fixture() 定义固件，下面是最简单的固件，只返回北京邮编：

'''


@pytest.fixture()
def postcode():
    return '010'


# 执行命令：pytest tests/test_textSummarization.py::test_postcode
def test_postcode(postcode):
    assert postcode == '010'


"""
预处理和后处理
很多时候需要在测试前进行预处理（如新建数据库连接），并在测试完成进行清理（关闭数据库连接）。

当有大量重复的这类操作，最佳实践是使用固件来自动化所有预处理和后处理。

Pytest 使用 yield 关键词将固件分为两部分，yield 之前的代码属于预处理，会在测试前执行；yield 之后的代码属于后处理，将在测试完成后执行。

以下测试模拟数据库查询，使用固件来模拟数据库的连接关闭：
"""


@pytest.fixture()
def db():
    print('Connection successful')

    yield

    print('Connection closed')


def search_user(user_id):
    d = {
        '001': 'xiaoming'
    }
    return d[user_id]


def test_search(db):
    assert search_user('001') == 'xiaoming'


"""
自动执行
目前为止，所有固件的使用都是手动指定，或者作为参数，或者使用 usefixtures。

如果我们想让固件自动执行，可以在定义时指定 autouse 参数。

下面是两个自动计时固件，一个用于统计每个函数运行时间（function 作用域），一个用于计算测试总耗时（session 作用域）：
"""
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nstart: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))


@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print(' Time cost: {:.3f}s'.format(time.time() - start))


def test_1():
    time.sleep(1)


def test_2():
    time.sleep(2)
