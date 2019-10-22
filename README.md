# Text-Auto-Summarization 文本自动摘要

![Languages](https://img.shields.io/badge/Languages-Python3.6-green)
![Build](https://img.shields.io/badge/Build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Contributions](https://img.shields.io/badge/Contributions-welcome-ff69b4.svg)


## 目前的摘要技术分为
1. Extraction 抽取式
2. Abstraction 生成式
```markdown
> 目前Extraction抽取式的主要方法：

>> - 基于统计：统计词频，位置等信息，计算句子权值，再简选取权值高的句子作为文摘，特点：简单易用，但对词句的使用大多仅停留在表面信息。

>> - 基于图模型：构建拓扑结构图，对词句进行排序。例如，TextRank/LexRank。

>> - 基于潜在语义：使用主题模型，挖掘词句隐藏信息。例如，采用LDA，HMM。

>> - 基于线路规划：将摘要问题转为线路规划，求全局最优解。

>> 在python语言中用于文本摘要自动提取的库包括goose，SnowNLP，TextTeaser，sumy，TextRank等。
```

## 项目使用指南

### git clone https://github.com/Valuebai/Text-Auto-Summarization.git
### 进入文件夹目录，使用下面的##Ptyhon创建虚拟环境 + ## Requirements 进行安装
### 服务器部署使用下面的## linux部署指南


## 项目效果
http://39.100.3.165:8188/TextSummarization/


## Textrank 和 Pagerank

[ipynb的地址]()


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


## Flask Blueprint，分隔视图
**当你的Flask项目膨胀到一定规模的时候， 全部都写到主入口之中。 一定需要按照模块进行拆分。 Blueprint(蓝图)就是这个时候需要使用的东西。**

- [Blueprint 之中使用日志](https://www.flyml.net/2018/12/12/flask-logging-usage-demo/)
- 完成blueprint框架后，在APP中的blueprint中
```python
from flask import current_app
# 在需要的地方
current_app.logger.info("simple page info...")
```



## Ptyhon创建虚拟环境

### 方法一：自带命令
1. 进入文件夹目录
2. python -m venv -h 可查看帮助信息
3. 下面的
```
Linux运行命令行
$ 创建默认环境：python3 -m venv my_venv 
$ 创建指定环境：python3.6 -m venv  my_venv,  python2 -m venv  my_venv(添加到系统环境变量中)
$ 激活环境：. my_venv/bin/activate  (. 或者 source )
$ 退出环境：deactivate 

Windows系统运行cmd，使用 "py" Python 启动器命令配合 "-m" 开关选项:
$ 创建环境：py -3 -m venv my_venv (或者python -m venv my_venv)
$ 创建指定环境：py -3.6 -m venv my_venv,  py -3.7 -m venv my_venv (添加到系统环境变量中)
$ 激活环境：my_venv\Scripts\activate.bat
$ 退出环境：deactivate

执行后，会在目录前方出现<my_venv>表明已进入虚拟环境

安装项目:
$ pip install -r requirements.txt
```

### 方法二：Windows在PyCharm下创建虚拟环境
1. 安装并激活PyCharm
这个请自行安装
官方地址：https://www.jetbrains.com/pycharm/

2. 在PyCharm下创建虚拟环境
第一步：点击New Project
第二步：选择下图的New environment
第三步：点击create即可
pycharm会为新创建的项目自动建立一个虚拟环境


### 方法三：conda创建虚拟环境

[anaconda中的常用操作](https://blog.csdn.net/CampusAmour/article/details/83215524)


Linux下启动其终端命令行 
$ source ~/anaconda3/bin/activate root
$ anaconda-navigator

- 创建虚拟环境，conda create -n env_name python=3.6

- 同时安装必要的包，conda create -n env_name numpy matplotlib python=3.6

- 激活虚拟环境
  - Linux：source activate your_env_name(虚拟环境名称)
  - Windows：activate your_env_name(虚拟环境名称)

- 退出虚拟环境： 
  - Linux：source deactivate your_env_name(虚拟环境名称)
  - Windows：deactivate your_env_name(虚拟环境名称)

- 删除虚拟环境，conda remove -n your_env_name(虚拟环境名称) --all
- 删除包使用命令，conda remove --name $your_env_name  $package_name（包名)


conda常用命令
- 查看已安装的包，conda list
- 安装包，conda install package_name(包名)
- 查看当前存在的虚拟环境，conda env list 或 conda info -e
- 检查更新当前conda，conda update conda

## Requirements
- 生成指南：
- 第一步：安装包 pip install pipreqs
- 第二步：在对应路径cmd，输入命令生成 requirements.txt文件：pipreqs ./ --encoding=utf8 --force 避免中文路径报错
- 第三步：下载该代码后直接pip install -r requirements.txt
- 或者创建虚拟环境安装

@[TOC](文章目录) #在CSDN自动生成目录

## linux部署指南
### 1. linux sh & nohup后台运行python脚本
  - 1）创建脚本vim run.sh
  - 2）填写内容并保存：nohup python3 -u  run.py > nohup.log 2>&1 &
  - 3）运行：sh run.sh 或者 . run.sh
  - 参考：[Linux sh、source和.命令执行.sh文件的区别](https://www.zengdongwu.com/article3.html) +
            [linux后台执行命令：&和nohup](https://blog.csdn.net/liuyanfeier/article/details/62422742)
```md
      - nohup : 就是不挂起的意思( no hang up)，可以在你退出帐户之后继续运行相应的进程
        - 使用&命令后，作业被提交到后台运行，当前控制台没有被占用，但是一但把当前控制台关掉(退出帐户时)，作业就会停止运行。nohup命令可以在你退出帐户之后继续运行相应的进程。
      - python3 -u  run.py : 执行py文件
      - -u的意思就是 uninterrupt不中断的意思，如果你的代码里边有sleep等线程沉睡相关的操作，如果你不-u的话 在后台 它就停住了
      - > nohup.log : 重定向保存日志到当前路径下的nohup.log
      - 2>&1 : 将标准出错也输出到nohup.log文件中
      - & : 最后一个&， 是让该命令在后台执行。
```

### 2. 使用gunicorn 部署flask服务 （个人项目推荐使用这个）
  - 1）创建脚本vim gunicorn.sh
  - 2）填写内容并保存：
    - conda activate just_do_it （在linux上创建好自己的环境，可选）
    - nohup gunicorn -w 4 -b 0.0.0.0:8001 run:app & （不带日志）
    - nohup gunicorn -w 4 -b 0.0.0.0:8001 run:app > gunicorn.log 2>&1 & （带日志）
    
  - 3）运行：sh gunicorn.sh 或者 . gunicorn.sh
  
```md
需要提前pip install gunicorn
简单地，gunicorn可以通过gunicorn -w 4 -b 0.0.0.0:8001 run:app启动一个Flask应用。其中,

-w 4是指预定义的工作进程数为4，
-b 127.0.0.1:4000指绑定地址和端口
run是flask的启动python文件，app则是flask应用程序实例

其中run.py中文件的可能形式是：
# run.py
from flask import Flask
app = Flask(__name__)

参考文章：
gunicorn部署Flask服务 https://www.jianshu.com/p/fecf15ad0c9a
https://www.cnblogs.com/gaidy/p/9784919.html
```

### 3. 使用screen命令部署
  - 第一步：screen -S yourname，新建一个叫yourname的session
  - 第二步：python run.py，运行代码，关闭shell连接后还会一直在linux上跑
  - 针对用户量小的情况，快速部署（本次使用这个）
  - 关于screen，详情见：https://www.cnblogs.com/mchina/archive/2013/01/30/2880680.html 
```
    杀死所有命令的：ps aux|grep 你的进程名|grep -v grep | awk '{print $2}'|xargs kill -9
    
    https://www.hutuseng.com/article/how-to-kill-all-detached-screen-session-in-linux
```

### 4. 使用flask + nginx + uwsgi (不建议，因Flask 与 uWsgi 结合有许多难以处理的 bug)
  - 针对用户访问量大的情况，具体参考下面的文章
    - https://blog.csdn.net/spark_csdn/article/details/80790929
    - https://www.cnblogs.com/Ray-liang/p/4173923.html
    - https://blog.csdn.net/daniel_ustc/article/details/9070357

### 5. 使用flask + nginx + gunicorn （大项目推荐使用这个）
  - 生产环境很多大公司采用这个方式的，故推荐这个
  - 因Flask 与 uWsgi 结合有许多难以处理的 bug，故推荐这个
  - [Flask + Gunicorn + Nginx 部署](https://www.cnblogs.com/Ray-liang/p/4837850.html)



## linux上杀死gunicorn的进程
**方法一**
1. netstat -nltp | grep 8188
能看到类似下面的：
tcp        0      0 0.0.0.0:8188            0.0.0.0:*               LISTEN      23422/gunicorn: mas

2. kill -9 23422（换成你的）


**方法二**
1. 获取Gunicorn进程树 
```
pstree -ap|grep gunicorn

得到的结果如下

Python
| | |-grep,14519 --color=auto gunicorn
| -gunicorn,28097 /usr/local/bin/gunicorn query_site.wsgi:application -c ... 
| |-gunicorn,14226 /usr/local/bin/gunicorn query_site.wsgi:application -c ... 
| | |-{gunicorn},14229 
| | |-{gunicorn},14230 
...

```

2. 重启Gunicorn任务

kill -HUP 14226

3. 退出Gunicorn任务

kill -9 28097


## linux根据端口号查找项目路径方法
### 1. 只知道端口号
1. 首先根据端口号查找进程
```
netstat -nltp
或者
netstat -nltp | grep python
或者
netstat -apn |grep 10010
```
2. 然后根据进程号去查找项目路径
```
ps -ef |grep 8567
```
3. 如果你第二步没有找到项目路径的话，尝试用
```
lsof -p 8567
```
### 2. 如果知道项目部署在tomcat里
如果你的项目在linux 中是部署到tomcat容器里，可以输入下边的命令找到，如下:
```
ps anx|grep tomcat
```






## Flask 快速完成前端页面


### 无法加载js, css等路径加载问题（在pycharm里面../ 没有报错，实际部署后404）

解决：将../ 改为 ./ ，因为是在text_blueprint.py文件启动的，python是动态加载，默认了此时的路径是text_blueprint.py的，用../会找不到对应的static
      
引申：在pycharm用../ 这种返回上一级的方法去单独执行一个文件，在pycharm里面是正常的，但是在windows命令行或者linux的部署中，是从run.py启动的，往往会出现这种情况


### 参考的页面
- https://github.com/MustAndy/AI_for_NLP/tree/master/Assi5/Project1_NLP_Become_human/code
一开始参考里面的js, html布局，前后端的交互


- https://github.com/zhangxu999/opinon_extraction 
- http://39.100.3.165:8421/index.html
Amazing4 zhangxu1573@qq.com
主页的模板套得很好看，学习里面的jquery


- https://github.com/4keyboardman/StandpointExtract 
- http://39.100.3.165:8871/
左右的布局很好看，还有的loading加载的学习


- http://39.100.3.165:8567/  

主页UI不好看，但是具体提取页面和生成树形图，学习了

有言论提取，文章摘要，情感分析


### D3.js (Data-Driven Documents) 数据可视化

[D3 的全称是（Data-Driven Documents），顾名思义可以知道是一个被数据驱动的文档。听名字有点抽象，说简单一点，其实就是一个 JavaScript 的函数库，使用它主要是用来做数据可视化的](http://wiki.jikexueyuan.com/project/d3wiki/introduction.html)