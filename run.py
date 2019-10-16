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
import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template, request

from APP.SpeechExtraction.speech_blueprint import app_extraction
from APP.TextSummarization.text_blueprint import app_summarization
from os.path import abspath, dirname

app = Flask("__main__", static_folder='static', template_folder='templates')

# 使用blueprint注册蓝图分隔视图
app.register_blueprint(app_extraction, url_prefix="/SpeechExtraction")
app.register_blueprint(app_summarization, url_prefix="/TextSummarization")
app.root_path = abspath(dirname(__file__))


# 展示网站主页
@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info("flask run~~")
    return render_template('main.html')


if __name__ == "__main__":
    app.debug = True

    # File and Console handler and formtter
    formatter = logging.Formatter(
        "[%(asctime)s][%(pathname)s: line(%(lineno)d)][%(levelname)s][thread:%(thread)d] - %(message)s")
    if not os.path.exists('./logs'):   os.mkdir('./logs')
    handler = TimedRotatingFileHandler(
        "./logs/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    # main run
    app.run(host='0.0.0.0', port=8188)
