#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/13 23:34
@Desc   ：
=================================================='''
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return ('this is project-02')


if __name__ == "__main__":
    print("this is project-02")
    app.run(host='0.0.0.0', debug=False, port=8188)
