# Text-Auto-Summarization 文本自动摘要

![Languages](https://img.shields.io/badge/Languages-Python3.6-green)
![Build](https://img.shields.io/badge/Build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Contributions](https://img.shields.io/badge/Contributions-welcome-ff69b4.svg)


## 目前的摘要技术分为
1. Extraction 抽取式
2. Abstraction 生成式

## Blueprint，分隔视图
**当你的Flask项目膨胀到一定规模的时候， 全部都写到主入口之中。 一定需要按照模块进行拆分。 Blueprint(蓝图)就是这个时候需要使用的东西。**

- [Blueprint 之中使用日志](https://www.flyml.net/2018/12/12/flask-logging-usage-demo/)
- 完成blueprint框架后，在APP中的blueprint中
```python
from flask import current_app
# 在需要的地方
current_app.logger.info("simple page info...")
```

## 部署指南
**1. linux sh & nohup后台运行脚本**
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

**2. 使用screen命令部署**
  - 第一步：screen -S yourname，新建一个叫yourname的session
  - 第二步：python run.py，运行代码，关闭shell连接后还会一直在linux上跑
  - 针对用户量小的情况，快速部署（本次使用这个）
  - 关于screen，详情见：https://www.cnblogs.com/mchina/archive/2013/01/30/2880680.html 
```
    杀死所有命令的：ps aux|grep 你的进程名|grep -v grep | awk '{print $2}'|xargs kill -9
    
    https://www.hutuseng.com/article/how-to-kill-all-detached-screen-session-in-linux
```
**3. 使用flask + nginx + uwsgi**
  - 针对用户访问量大的情况，具体参考下面的文章
    - https://blog.csdn.net/spark_csdn/article/details/80790929
    - https://www.cnblogs.com/Ray-liang/p/4173923.html
    - https://blog.csdn.net/daniel_ustc/article/details/9070357


**4. 使用gunicorn 部署flask服务
  - 1）创建脚本vim gunicorn.sh
  - 2）填写内容并保存：
    - conda activate just_do_it （在linux上创建好自己的环境，可选）
    - nohup gunicorn -w 4 -b 0.0.0.0:8001 run:app & （不带日志）
    - nohup gunicorn -w 4 -b 0.0.0.0:8001 run:app > gunicorn.log 2>&1 & （带日志）
    
  - 3）运行：sh gunicorn.sh 或者 . gunicorn.sh
  
```md
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






## requirements.txt
- 生成指南：
- 第一步：安装包 pip install pipreqs
- 第二步：在对应路径cmd，输入命令生成 requirements.txt文件：pipreqs ./ --encoding=utf8 --force 避免中文路径报错
- 第三步：下载该代码后直接pip install -r requirements.txt


## linux 知识学习-根据端口号查找项目路径方法
### 只知道端口号
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
### 如果知道项目部署在tomcat里
如果你的项目在linux 中是部署到tomcat容器里，可以输入下边的命令找到，如下:
```
ps anx|grep tomcat
```


## flask 快速完成前端页面

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