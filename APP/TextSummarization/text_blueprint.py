#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/16 22:34
@Desc   ：
=================================================='''
import json
from flask import request, render_template, jsonify, Blueprint
from flask import current_app
from APP.TextSummarization.textrank.textrank4zh_run import get_textrank4zh_keywords, get_textrank4zh_summarization

app_summarization = Blueprint("autosummarization", __name__, static_folder='static', template_folder='templates')


@app_summarization.route('/', methods=["GET"])
def index():
    current_app.logger.info("run app_summarization")
    return 'app_summarization'


# 关键字提取
@app_summarization.route('/keyword', methods=['GET', 'POST'])
def extract_keyword():
    try:
        # prefix = request.json.get
        print('test1', request.form)
        prefix = request.form['keyword']
        current_app.logger.info('前端输入的文本为：{}'.format(prefix))
        result = get_textrank4zh_keywords(prefix)
        res = {'code': 1, 'message': '数据获取成功', 'data': result}
    except Exception as e:
        current_app.logger.error(e)
        res = {'code': 0, 'message': '系统内部错误，请联系管理员', 'data': ''}

    return json.dumps(res, ensure_ascii=False, indent=4)


# 文本摘要提取
@app_summarization.route('/summarization', methods=['GET', 'POST'])
def extract_summarization():
    try:
        # prefix = request.json.get('prefix')
        prefix = request.form['summarization']
        result = get_textrank4zh_summarization(prefix)
        res = {'code': 1, 'message': '数据获取成功', 'data': result}
    except Exception as e:
        current_app.logger.error(e)
        res = {'code': 0, 'message': '系统内部错误，请联系管理员', 'data': ''}

    return json.dumps(res, ensure_ascii=False, indent=4)
