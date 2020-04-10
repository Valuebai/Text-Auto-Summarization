#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2019/4/2 14:46
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
"""
    封装python logging日志，命名为log_config.py
    ~~~~~~~~~~~~~~~

    - 修改日志保存路径，否则使用默认上一层目录的./logs/
    - 使用：from common.log_config import logger     # common表示本文件放在的文件夹
        logger.info('打印info日志')
        logger.error('打印error日志')


    注意：
    - flask 有自带的log，使用本文件后会覆盖flask自带的

    - 无法自动删除日志 & 日志没有分隔记录
      使用TimedRotatingFileHandler创建时间循环日志，suffix需写成对应格式，如下
      参数中的when="D", or MIDNIGHT 天，file_handler.suffix = "%Y-%m-%d.log"
      参数中的when="S" 秒，file_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"

    - 多进程写入同一日志文件冲突问题
      >> PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问。

      >> 类似：2.使用多进程初始化同一日志模块，会导致日志备份报错，因为两个进程同时打开了日志文件，在重命名时会出现
                 WindowsError: [Error 32]错误，该错误是由于文件已被打开，
        按照官方文档的介绍，logging 是线程安全的，也就是说，在一个进程内的多个线程同时往同一个文件写日志是安全的。但是（对，
        这里有个但是）多个进程往同一个文件写日志不是安全的,为了解决这个问题，可使用 ConcurrentLogHandler，
        ConcurrentLogHandler 可以在多进程环境下安全的将日志写入到同一个文件，并且可以在日志文件达到特定大小时，分割日志文件。
      >> 在默认的 logging 模块中，有个 TimedRotatingFileHandler 类，可以按时间分割日志文件，
        可惜 ConcurrentLogHandler 不支持这种按时间分割日志文件的方式。(用单例模式无法解决!)

      >> 解决方法：1、继承TimedRotatingFileHandler重载，修改里面的东西
      >> 解决方法：2、直接使用开源的代码来用，本文使用的是concurrent_log  ！！！
                     安装：pip install concurrent_log
                     url: https://github.com/huanghyw/concurrent_log
                     使用from concurrent_log import ConcurrentTimedRotatingFileHandler
                     直接在用TimedRotatingFileHandler替换为ConcurrentTimedRotatingFileHandler即可，其他代码不需要任何改动

                    - 下面的代码中的
                    - class ConcurrentLogFileLock(PortaLock):
                    - class ConcurrentTimedRotatingFileHandler(TimedRotatingFileHandler):
                    - 是来自ConcurrentTimedRotatingFileHandler

      >> 解决方法：3、建议使用sentry 来记录日志
"""

import os
import re
import time
import logging
import logging.config
import logging.handlers
import portalocker.constants as porta_lock_const
from logging.handlers import TimedRotatingFileHandler
from portalocker.utils import Lock as PortaLock


class ConcurrentLogFileLock(PortaLock):
    """
    这个类来自：ConcurrentTimedRotatingFileHandler
    解决方法：2、直接使用开源的代码来用，本文使用的是concurrent_log
    """

    def __init__(self, filename, *args, **kwargs):
        PortaLock.__init__(self, self.get_lock_filename(filename), *args, **kwargs)

    def get_lock_filename(self, log_file_name):
        """
        定义日志文件锁名称，类似于 `.__file.lock`，其中file与日志文件baseFilename一致
        :return: 锁文件名称
        """
        if log_file_name.endswith(".log"):
            lock_file = log_file_name[:-4]
        else:
            lock_file = log_file_name
        lock_file += ".lock"
        lock_path, lock_name = os.path.split(lock_file)
        # hide the file on Unix and generally from file completion
        lock_name = ".__" + lock_name
        return os.path.join(lock_path, lock_name)


class ConcurrentTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    这个类来自：ConcurrentTimedRotatingFileHandler
    解决方法：2、直接使用开源的代码来用，本文使用的是concurrent_log
    """
    # 上一次翻转时间
    before_rollover_at = -1

    def __init__(self, filename, *args, **kwargs):
        TimedRotatingFileHandler.__init__(self, filename, *args, **kwargs)

        file_path = os.path.split(filename)[0]
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        self.concurrent_lock = ConcurrentLogFileLock(filename, flags=porta_lock_const.LOCK_EX)

    def emit(self, record) -> None:
        """
        本方法继承Python标准库,修改的部分已在下方使用注释标记出
        本次改动主要是对日志文件进行加锁，并且保证在多进程环境下日志内容切割正确
        """
        # 此行为新增代码，尝试获取非重入进程锁，阻塞，直到成功获取
        with self.concurrent_lock:
            try:
                if self.shouldRollover(record):
                    self.doRollover()

                """
                如果日志内容创建时间小于上一次翻转时间，不能记录在baseFilename文件中，否则正常记录

                处理日志写入哪个日志文件，修改开始
                """
                if record.created <= ConcurrentTimedRotatingFileHandler.before_rollover_at:
                    currentTime = int(record.created)
                    # v 引用Python3.7标准库logging.TimedRotatingFileHandler.doRollover(110:124)中翻转目标文件名生成代码 v
                    dstNow = time.localtime(currentTime)[-1]
                    t = self.computeRollover(currentTime) - self.interval
                    if self.utc:
                        timeTuple = time.gmtime(t)
                    else:
                        timeTuple = time.localtime(t)
                        dstThen = timeTuple[-1]
                        if dstNow != dstThen:
                            if dstNow:
                                addend = 3600
                            else:
                                addend = -3600
                            timeTuple = time.localtime(t + addend)
                    dfn = self.rotation_filename(self.baseFilename + "." +
                                                 time.strftime(self.suffix, timeTuple))
                    # ^ 引用标准库TimedRotatingFileHandler中翻转目标文件名生成规则代码                                  ^

                    # 如果back_count值设置的过低，会出现日志文件实际数量大于设置值
                    # 因为当日志写入负载过高时，之前的某个时刻产生的日志会延迟到现在才进行写入，在写入时又找不到与时间对应的日志文件，
                    # 则会再创建一个与日志创建时刻对应的日志文件进行写入。
                    # 对应的日志文件是指达到翻转条件后创建的翻转文件，文件命名规则与标准库一致。
                    self._do_write_record(dfn, record)
                else:
                    logging.FileHandler.emit(self, record)
                """
                处理日志写入哪个日志文件，修改结束
                """
            except Exception:
                self.handleError(record)

    def doRollover(self):
        """
        本方法继承Python标准库,修改的部分已在下方使用注释标记出
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))
        """
        如果翻转文件已经生成，则说明其他进程已经处理过翻转
        处理日志文件已经翻转当前进程中未写入文件的日志副本，修改开始
        """
        # 直接修改静态变量，因为代码执行到此处已经获取到非重入进程锁，保证同一时间只有一个线程对变量进行修改
        # 由于Python GIL，同一时间同一进程内只有一个线程运行，线程切换后缓存自动失效，即其他线程可以看见修改后的最新值
        # 记录每一次触发翻转动作的时间，不管反转是否真的执行
        ConcurrentTimedRotatingFileHandler.before_rollover_at = self.rolloverAt
        if os.path.exists(dfn):
            # 因为进程变量不会在内存同步，所以存在其他进程已经翻转过日志文件当时当前进程中还标识为未翻转
            # 日志内容创建时间如果小于等于下一个处理翻转时刻，则将日志写入反转后的日志文件，而不是当前的baseFilename
            # 当前磁盘上的baseFilename对于当前进程中的标识副本来说已经是翻转后要写入的文件
            # 所以当文件存在时，本次不再进行翻转动作
            pass
        else:
            self.rotate(self.baseFilename, dfn)
        """
        处理日志文件已经翻转当前进程中未写入文件的日志副本，修改结束
        """
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        # 此刻，当前进程中的标识副本已经同步为最新
        self.rolloverAt = newRolloverAt

    def _do_write_record(self, dfn, record):
        """
        将日志内容写入指定文件
        :param dfn: 指定日志文件
        :param record: 日志内容
        """
        with open(dfn, mode="a", encoding=self.encoding) as file:
            file.write(self.format(record) + self.terminator)


class GetLogger:
    """
    自定义logging，方便使用
    """

    def __init__(self, logs_dir=None, logs_level=logging.INFO):
        self.logs_dir = logs_dir  # 日志路径
        self.log_name = r'app.log'  # 日志名称
        self.logs_level = logs_level  # 日志级别
        # 日志的输出格式
        self.log_formatter = logging.Formatter(
            '%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] [%(lineno)d] %(message)s')

        if logs_dir is None:
            sep = os.sep  # 自动匹配win,mac,linux 下的路径分隔符
            self.logs_dir = os.path.abspath(
                os.path.join(__file__, f"..{sep}..{sep}logs{sep}"))  # 设置日志保存路径

        # 如果logs文件夹不存在，则创建
        if os.path.exists(self.logs_dir) is False:
            os.mkdir(self.logs_dir)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        # 实例化root日志对象
        log_logger = logging.getLogger('root')

        # 设置日志的输出级别
        log_logger.setLevel(self.logs_level)
        if not log_logger.handlers:  # 避免重复日志
            # 创建一个handler，用于输出到cmd窗口控制台
            console_handler = logging.StreamHandler()

            console_handler.setLevel(logging.INFO)  # 设置日志级别
            console_handler.setFormatter(self.log_formatter)  # 设置日志格式
            log_logger.addHandler(console_handler)

            # 建立一个循环文件handler来把日志记录在文件里
            file_handler = ConcurrentTimedRotatingFileHandler(
                filename=self.logs_dir + os.sep + self.log_name,  # 定义日志的存储
                when="MIDNIGHT",  # 按照日期进行切分when = D： 表示按天进行切分,or self.when == 'MIDNIGHT'
                interval=1,  # interval = 1： 每天都切分。 比如interval = 2就表示两天切分一下。
                backupCount=30,  # 最多存放日志的数量
                encoding="UTF-8",  # 使用UTF - 8的编码来写日志
                delay=False,
                utc=False  # 使用UTC + 0的时间来记录 （一般docker镜像默认也是UTC + 0）
            )
            file_handler.suffix = "%Y-%m-%d.log"
            # need to change the extMatch variable to match the suffix for it
            file_handler.extMatch = re.compile(r"^\d{8}$")
            file_handler.setLevel(logging.DEBUG)  # 设置日志级别
            file_handler.setFormatter(self.log_formatter)  # 设置日志格式
            file_handler.doRollover()
            log_logger.addHandler(file_handler)

        return log_logger


logging.handlers.ConcurrentTimedRotatingFileHandler = ConcurrentTimedRotatingFileHandler
logger = GetLogger().get_logger()

if __name__ == "__main__":
    # 对上面代码进行测试
    logger = GetLogger().get_logger()

    # 在具体需要的地方
    logger.info('INFO日志打印...')
    logger.error('ERROR日志打印...')

    # # 打印日志保存路径
    # sep = os.sep
    # set_log_path = os.path.abspath(
    #     os.path.join(__file__, f"..{sep}..{sep}logs{sep}"))
    # print('测试Log路径：', set_log_path)

    import time

    while True:
        logger.info('每隔X打印一下')
        time.sleep(2)
