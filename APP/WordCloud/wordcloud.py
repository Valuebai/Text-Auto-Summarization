#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/15 15:17
@Desc   ：
=================================================='''

import pandas as pd

import numpy as np
from opencc import OpenCC   #opencc无法在py3.6.5安装，后面把代码替换成我之前写过的
import jieba
from wordcloud import WordCloud


def is_CN_char(ch):
    return ch >= u'\u4e00' and ch <= u'\u9fa5'


def cut(string):
    return list(jieba.cut(string))


def get_stopwords(filename="D:/senior/aiCourse/dataSource/stop_word.txt"):
    stopwords_dic = open(filename, encoding='utf-8')
    stopwords = stopwords_dic.readlines()
    stopwords = [w.strip() for w in stopwords]
    stopwords_dic.close()
    return stopwords


def convert2simple(word):
    openCC = OpenCC('tw2sp')
    return openCC.convert(word)


def clean_sentence(sentence):
    stopwords = get_stopwords()
    sentence = ''.join(filter(is_CN_char, sentence))
    # print(sentence)

    sentence = convert2simple(sentence)
    words = [w for w in cut(sentence) if len(w) > 0 and w not in stopwords]
    # print(words)
    words = ' '.join(words)
    return words


import multiprocessing as mp
import time


def worker(iteration, sub_data, q):
    """worker function"""
    num = 10000
    result = sub_data[(iteration * num):(iteration + 1) * num]['content'].apply(clean_sentence)
    print('finished')
    q.put(''.join(result.tolist()))
    return result


if __name__ == '__main__':
    stopwords = get_stopwords()
    data = pd.read_csv('D:/senior/aiCourse/dataSource/comment_classification/train/sentiment_analysis_trainingset.csv',
                       encoding='UTF-8')
    # 填充空白格
    data['content'] = data['content'].fillna('')
    sample = 100000
    random_indices = np.random.choice(np.arange(len(data['content'])), sample)
    sub_data = data.iloc[random_indices]
    q = mp.Queue()
    jobs = []
    for i in range(9):
        p = mp.Process(target=worker, args=[i, sub_data, q])
        jobs.append(p)
        p.start()

    resultALL = []
    for i in range(9):
        resultALL.append(q.get())

    wc = WordCloud(background_color='white', font_path='D://senior/aiCourse/dataSource/SourceHanSerifSC-Regular.otf')
    worddata = ''.join(resultALL)
    print("generating...")
    wc.generate_from_text(worddata)

    wc.to_file('comment_wc.png')
