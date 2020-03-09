# shell杀死指定端口的进程，写到部署脚本里面
kill -9 $(netstat -nlp | grep :8188 | awk '{print $7}' | awk -F"/" '{ print $1 }')

# 另一个启动方式nohup python3 -u  run.py > nohup.log 2>&1 &
# 后台运行
nohup gunicorn -w 4 -b 0.0.0.0:8188 run:app > gunicorn.log 2>&1 &
