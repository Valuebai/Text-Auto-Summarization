#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/22 14:45
@Desc   ：
## 本地&线上同步推进（后续优化）
### 业务场景
本地与线上的 Swagger API 文档的接口的地址是不同的，但都依赖同一个配置文件 **`app\config\setting.py`**。<br>
而个人项目有着本地和线上同步，开发和测试同步的需求，会不断修改 **`app\config\setting.py`** 文件，无法用 **`.gitignore`** 做到忽略配置文件，本地和线上配置隔离的效果。

### 解决
**`本地`** 和 **`线上`** 自动根据所处的环境(由 .gitignore 控制)不同，选择不同的配置文件。<br>
那么， **`本地`** 可以比 **`线上`** 多了 **`app/config/dev.py`** 文件; 基于该文件的存在与否，可以用 **`if else`** 控制 **`app/config/`** 中配置输出。

### Demo
1. `echo "/app/config/dev.py" >> .gitignore` # 追加 Git 忽略提交配置到 .gitignore
2. 新建 **`app/config/dev.py`** 文件

=================================================='''
import os

is_dev_mode = os.path.exists('./conf/dev.py')  # 'development' & 'product' (开发环境 or 生产环境)

EXTERNAL_URL = 'server.mini-shop.ivinetrue.com'  # 外部（云服务器）地址
INTERNAL_URL = '0.0.0.0:8080'  # 内部（本地）地址
SERVER_URL = INTERNAL_URL if is_dev_mode else EXTERNAL_URL

EXTERNAL_SCHEMES = ["https", "http"]  # 外部（云服务器）支持 https 和 http 协议
INTERNAL_SCHEMES = ["http"]  # 内部只支持http
SERVER_SCHEMES = INTERNAL_SCHEMES if is_dev_mode else EXTERNAL_SCHEMES

IMG_PREFIX = SERVER_URL + '/static/images'
UPLOAD_FOLDER = 'app/static/uploads'
VERSION = "0.3.0"  # 项目版本

if __name__ == '__main__':
    # 在上一层的run.py文件，使用os.path.exists('./conf/dev.py')
    # 直接运行本运行测试，使用os.path.exists('./dev.py')
    print(is_dev_mode)
