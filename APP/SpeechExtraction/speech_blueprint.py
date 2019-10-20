#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/16 22:32
@Desc   ：
=================================================='''

from flask import request, render_template, jsonify, Blueprint
# from flask import current_app

app_extraction = Blueprint("speech_extraction", __name__, static_folder='static', template_folder='templates')
from conf.logConf import logger


@app_extraction.route('/')
def index():
    logger.info('speech_extraction')
    return 'app_extraction'
