#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/24 18:16
@Desc   ：
=================================================='''

import jieba
import numpy as np
import collections
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def split_sentence(text, punctuation_list='!?。！？'):
    """
    将文本段安装标点符号列表里的符号切分成句子，将所有句子保存在列表里。
    """
    sentence_set = []
    inx_position = 0  # 索引标点符号的位置
    char_position = 0  # 移动字符指针位置
    for char in text:
        char_position += 1
        if char in punctuation_list:
            next_char = list(text[inx_position:char_position + 1]).pop()
            if next_char not in punctuation_list:
                sentence_set.append(text[inx_position:char_position])
                inx_position = char_position
    if inx_position < len(text):
        sentence_set.append(text[inx_position:])

    sentence_with_index = {i: sent for i, sent in
                           enumerate(sentence_set)}  # dict(zip(sentence_set, range(len(sentences))))
    return sentence_set, sentence_with_index


def get_tfidf_matrix(sentence_set, stop_word):
    corpus = []
    for sent in sentence_set:
        sent_cut = jieba.cut(sent)
        sent_list = [word for word in sent_cut if word not in stop_word]
        sent_str = ' '.join(sent_list)
        corpus.append(sent_str)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    # word=vectorizer.get_feature_names()
    tfidf_matrix = tfidf.toarray()
    return np.array(tfidf_matrix)


def get_sentence_with_words_weight(tfidf_matrix):
    sentence_with_words_weight = {}
    for i in range(len(tfidf_matrix)):
        sentence_with_words_weight[i] = np.sum(tfidf_matrix[i])

    max_weight = max(sentence_with_words_weight.values())  # 归一化
    min_weight = min(sentence_with_words_weight.values())
    for key in sentence_with_words_weight.keys():
        x = sentence_with_words_weight[key]
        sentence_with_words_weight[key] = (x - min_weight) / (max_weight - min_weight)

    return sentence_with_words_weight


def get_sentence_with_position_weight(sentence_set):
    sentence_with_position_weight = {}
    total_sent = len(sentence_set)
    for i in range(total_sent):
        sentence_with_position_weight[i] = (total_sent - i) / total_sent
    return sentence_with_position_weight


def similarity(sent1, sent2):
    """
    计算余弦相似度
    """
    return np.sum(sent1 * sent2) / 1e-6 + (np.sqrt(np.sum(sent1 * sent1)) * \
                                           np.sqrt(np.sum(sent2 * sent2)))


def get_similarity_weight(tfidf_matrix):
    sentence_score = collections.defaultdict(lambda: 0.)
    for i in range(len(tfidf_matrix)):
        score_i = 0.
        for j in range(len(tfidf_matrix)):
            score_i += similarity(tfidf_matrix[i], tfidf_matrix[j])
        sentence_score[i] = score_i

    max_score = max(sentence_score.values())  # 归一化
    min_score = min(sentence_score.values())
    for key in sentence_score.keys():
        x = sentence_score[key]
        sentence_score[key] = (x - min_score) / (max_score - min_score)

    return sentence_score


def ranking_base_on_weigth(sentence_with_words_weight,
                           sentence_with_position_weight,
                           sentence_score, feature_weight=[1, 1, 1]):
    sentence_weight = collections.defaultdict(lambda: 0.)
    for sent in sentence_score.keys():
        sentence_weight[sent] = feature_weight[0] * sentence_with_words_weight[sent] + \
                                feature_weight[1] * sentence_with_position_weight[sent] + \
                                feature_weight[2] * sentence_score[sent]

    sort_sent_weight = sorted(sentence_weight.items(), key=lambda d: d[1], reverse=True)
    return sort_sent_weight


def get_summarization(sentence_with_index, sort_sent_weight, topK_ratio=0.3):
    topK = int(len(sort_sent_weight) * topK_ratio)
    print('topK:{0}'.format(topK))
    summarization_sent = sorted([sent[0] for sent in sort_sent_weight[:topK]])

    summarization = []
    for i in summarization_sent:
        summarization.append(sentence_with_index[i])

    summary = ''.join(summarization)
    return summary


if __name__ == '__main__':
    # test_text = '../../data/training17.txt'
    # with open(test_text, 'r', encoding='utf-8') as f:
    #     text = f.read()

    text = '''网易娱乐7月21日报道 林肯公园主唱查斯特·贝宁顿Chester Bennington于今天早上，在洛杉矶帕洛斯弗迪斯的一个私人庄园自缢身亡，年仅41岁。此消息已得到洛杉矶警方证实。

    　　洛杉矶警方透露，Chester的家人正在外地度假，Chester独自在家，上吊地点是家里的二楼。一说是一名音乐公司工作人员来家里找他时发现了尸体，也有人称是佣人最早发现其死亡。

    　　林肯公园另一位主唱麦克·信田确认了Chester Bennington自杀属实，并对此感到震惊和心痛，称稍后官方会发布声明。Chester昨天还在推特上转发了一条关于曼哈顿垃圾山的新闻。粉丝们纷纷在该推文下留言，不相信Chester已经走了。
    　　外媒猜测，Chester选择在7月20日自杀的原因跟他极其要好的朋友、Soundgarden(声音花园)乐队以及Audioslave乐队主唱Chris Cornell有关，因为7月20日是Chris Cornell的诞辰。而Chris Cornell于今年5月17日上吊自杀，享年52岁。Chris去世后，Chester还为他写下悼文。
    　　对于Chester的自杀，亲友表示震惊但不意外，因为Chester曾经透露过想自杀的念头，他曾表示自己童年时被虐待，导致他医生无法走出阴影，也导致他长期酗酒和嗑药来疗伤。目前，洛杉矶警方仍在调查Chester的死因。
    　　据悉，Chester与毒品和酒精斗争多年，年幼时期曾被成年男子性侵，导致常有轻生念头。Chester生前有过2段婚姻，育有6个孩子。
    　　林肯公园在今年五月发行了新专辑《多一丝曙光One More Light》，成为他们第五张登顶Billboard排行榜的专辑。而昨晚刚刚发布新单《Talking To Myself》MV。'''

    stop_word = []

    # 这个停用词表增加了很多中文的
    with open('../../data/stopWordList.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            stop_word.append(line.strip())

    sentence_set, sentence_with_index = split_sentence(text, punctuation_list='!?。！？')
    tfidf_matrix = get_tfidf_matrix(sentence_set, stop_word)
    sentence_with_words_weight = get_sentence_with_words_weight(tfidf_matrix)
    sentence_with_position_weight = get_sentence_with_position_weight(sentence_set)
    sentence_score = get_similarity_weight(tfidf_matrix)
    sort_sent_weight = ranking_base_on_weigth(sentence_with_words_weight,
                                              sentence_with_position_weight,
                                              sentence_score, feature_weight=[1, 1, 1])
    summarization = get_summarization(sentence_with_index, sort_sent_weight, topK_ratio=0.3)
    print('summarization:\n', summarization)
