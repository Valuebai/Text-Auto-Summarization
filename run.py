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
from flask import Flask, render_template

from APP.SpeechExtraction.speech_blueprint import app_extraction
from APP.TextSummarization.text_blueprint import app_summarization
from os.path import abspath, dirname
from conf.logConf import logger
from conf.setting import is_dev_mode
import jieba

app = Flask("__main__", static_folder='static', template_folder='templates')

# 使用blueprint注册蓝图分隔视图
app.register_blueprint(app_extraction, url_prefix="/SpeechExtraction")
app.register_blueprint(app_summarization, url_prefix="/TextSummarization")
app.root_path = abspath(dirname(__file__))


# 展示网站主页
@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info('访问home.html')
    logger.info("$_$ kill_bug_team run, to the moon $_$")
    return render_template('home.html')


if __name__ == "__main__":
    app.debug = True
    jieba.initialize()
    logger.info('项目运行，GO')
    logger.info('is_dev_mode:{}'.format(is_dev_mode))
    # main run
    app.run(host='0.0.0.0', port=8188)


