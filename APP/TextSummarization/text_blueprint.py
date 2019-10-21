#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/16 22:34
@Desc   ：
=================================================='''
import os
import json
from flask import request, render_template, jsonify, Blueprint
# from flask import current_app
from APP.TextSummarization.textrank.textrank4zh_run import get_textrank4zh_keywords, get_textrank4zh_summarization_str
from conf.logConf import logger

# setting up template directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app_summarization = Blueprint("autosummarization", __name__, static_folder=ASSETS_DIR, template_folder='templates')


@app_summarization.route('/', methods=["GET"])
def index():
    logger.info("run app_summarization")
    return render_template('pro2.html')


# 文本摘要提取
@app_summarization.route('/show', methods=['POST'])
def extract_summarization():
    try:
        data = request.json
        text = data['text']

        # 判断文本的类型，如果是bytes，则转换为utf-8
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        # 去掉文本中的全角空白符，不间断空白符 &nbsp;，字节顺序标记，换行
        text = text.replace('\u3000', '').replace('\xa0', '').replace('\ufeff', '').replace('\n', '').replace('\\n', '')

        # 获取文本摘要
        result_summarization = get_textrank4zh_summarization_str(text)
        # 获取文本关键字
        result_keywords = get_textrank4zh_keywords(text)

        # 封装为字典
        res = {'code': 1, 'message': '数据获取成功', 'keywords': result_keywords, 'summarization': result_summarization}
        logger.info('/show接口数据获取成功')

    except Exception as e:
        logger.error(e)
        res = {'code': 0, 'message': '系统内部错误，请联系管理员', 'data': ''}

    return json.dumps(res, ensure_ascii=False, indent=4)
