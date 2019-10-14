# Text-Auto-Summarization 文本自动摘要

![Languages](https://img.shields.io/badge/Languages-Python3.6-green)
![Build](https://img.shields.io/badge/Build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Contributions](https://img.shields.io/badge/Contributions-welcome-ff69b4.svg)


## 目前的摘要技术分为
1. Extraction 抽取式
2. Abstraction 生成式



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








## requirements.txt
- 生成指南：
- 第一步：安装包 pip install pipreqs
- 第二步：在对应路径cmd，输入命令生成 requirements.txt文件：pipreqs ./ --encoding=utf8 --force 避免中文路径报错
- 第三步：下载该代码后直接pip install -r requirements.txt
