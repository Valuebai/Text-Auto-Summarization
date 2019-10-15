#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/13 23:34
@Desc   ：

---
flask 的日志打印：app.logger.info("Info message")
按照日期进行切分
when=D： 表示按天进行切分
interval=1： 每天都切分。 比如interval=2就表示两天切分一下。
backupCount=15: 保留15天的日志
encoding=UTF-8: 使用UTF-8的编码来写日志
utc=True: 使用UTC+0的时间来记录 （一般docker镜像默认也是UTC+0）
=================================================='''
import logging
from logging.handlers import TimedRotatingFileHandler

import json
from flask import Flask, render_template, request
from textrank.textrank_jieba import getKeywords_textrank
from textrank.textrank4zh_run import get_textrank4zh_summarization

app = Flask(__name__)


@app.route('/')
def index():
    app.logger.info("Info message")
    app.logger.warning("Warning msg")
    app.logger.error("Error msg!!!")
    return 'ok'


# 关键字提取
@app.route('/extract/keyword', methods=['GET'])  # 后面需要改为post
def extract_keyword():
    try:
        prefix = request.json.get('prefix')
        result = getKeywords_textrank(prefix)
        res = {'code': 1, 'message': '数据获取成功', 'data': result}
    except Exception as e:
        app.logger.error(e)
        res = {'code': 0, 'message': '系统内部错误，请联系管理员', 'data': ''}

    return json.dumps(res, ensure_ascii=False, indent=4)


# 文本摘要提取
@app.route('/extract/summarization', methods=['GET'])  # 后面需要改为post
def extract_summarization():
    try:
        prefix = request.json.get('prefix')
        result = get_textrank4zh_summarization(prefix)
        res = {'code': 1, 'message': '数据获取成功', 'data': result}
    except Exception as e:
        app.logger.error(e)
        res = {'code': 0, 'message': '系统内部错误，请联系管理员', 'data': ''}

    return json.dumps(res, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app.debug = True
    formatter = logging.Formatter(
        "[%(asctime)s][%(pathname)s: line(%(lineno)d)][%(levelname)s][thread:%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "./log/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    app.run(host='0.0.0.0', port=8188)
