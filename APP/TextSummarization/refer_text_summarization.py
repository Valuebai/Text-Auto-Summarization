#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/23 18:29
@Desc   ：
=================================================='''
from gensim.models import KeyedVectors
import numpy as np
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from pyltp import SentenceSplitter
import pickle

import re
import jieba
import operator
from functools import reduce
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import gc


class SentenceEmbedding:
    # 句子向量化类
    def __init__(self):
        self.word_frequence = self.__get_word_frequence()

    def get_sentences_vec(self, model_wv, sent_list):
        # 句子向量化处理
        a = 0.001
        row = model_wv.vector_size
        col = len(sent_list)
        sent_mat = np.zeros((row, col))
        for i, sent in enumerate(sent_list):
            length = len(sent)
            if length == 0: continue
            sent_vec = np.zeros(row)
            for word in sent:
                pw = self.word_frequence[word]
                if pw == 0: continue
                w = a / (a + pw)
                # print(w)
                try:
                    vec = np.array(model_wv[word])
                    sent_vec += w * vec
                except:
                    pass
            sent_mat[:, i] += sent_vec
            sent_mat[:, i] /= length

        # PCA处理
        # print(sent_mat.shape)

        sent_mat = np.mat(sent_mat)
        u, s, vh = np.linalg.svd(sent_mat)
        sent_mat = sent_mat - u * u.T * sent_mat
        return sent_mat

    def __get_word_frequence(self):
        # 这里不做停用次处理，直接在计算句子向量时候，如果找不到该词，直接跳过
        path = Myconfig.get_path('frequency.txt')
        assert path
        with open(path, 'rb') as f:
            word_frequence = pickle.load(f)
        return word_frequence

    # 计算余弦相似度
    def cos_similarity(self, v1, v2):
        assert isinstance(v1, np.ndarray)
        assert isinstance(v2, np.ndarray)
        # 输入向量维度不一致
        if len(v1) != len(v2):
            return 0
        if np.linalg.norm(v2) == 0 or np.linalg.norm(v1) == 0:
            return 0
        return np.vdot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    # 返回句子向量矩阵中各列向量与第一列向量的相似度
    def __calcu_similarity(self, sent_mat):
        assert (isinstance(sent_mat, np.ndarray) or isinstance(sent_mat, np.matrix))
        # 采用点积的方法计算
        first = np.array(sent_mat[:, 0]).flatten()
        col = sent_mat.shape[1]
        sims = []
        for i in range(1, col):
            vec = np.array(sent_mat[:, i]).flatten()
            sims.append(self.cos_similarity(first, vec))
        return sims

    # 获取相似度结果#输入句子中每一句和首句的相似度
    def get_similarity_result(self, model_wv, sent_list):
        sent_mat = self.get_sentences_vec(model_wv, sent_list)
        sim = self.__calcu_similarity(sent_mat)
        return sim


# def test(sens, sim):
#     print('##################################')
#     index = list(np.argsort(sim))
#     index.reverse()
#     for i in index:
#         print(sim[i], sens[i])


class Summarization:
    def __init__(self):
        self.position_re_weight = True
        self.Sen_Embedding = SentenceEmbedding()
        self.stopwords = self.__get_stopwords()
        fname = Myconfig.get_path('vec.kv')  # 或取模型目录
        assert fname
        self.model_wv = KeyedVectors.load(fname, mmap='r')

    def __get_stopwords(self):
        path = Myconfig.get_path('stopwords.txt')
        stopwords = []
        with open(path, encoding='GBK') as f:
            line = f.readline()
            while line != '':
                stopwords.append(line.strip('\n'))
                line = f.readline()
        stopwords.append(' ')
        return set(stopwords)

    def __get_keyword(self, string):
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=string, lower=True, window=4)
        keyword_items = tr4w.get_keywords(10, word_min_len=2)
        # 把权重标准化
        keyword_items = sorted(keyword_items, key=lambda x: x.weight)
        over_length = keyword_items[-1].weight
        for wp in keyword_items:
            wp.weight /= over_length
        return keyword_items

    # 用正则表达式进行切句
    def __split_sentence(self, string):
        pattern = re.compile('[。，,.?？!！""“”]')
        pattern1 = re.compile('\w+?([。，,.?？!！""“”])')
        flags = pattern1.findall(string)
        sentences = pattern.sub('***', string).split('***')
        sentences = [sen for sen in sentences if sen != '']
        if (len(sentences) > len(flags)): flags.append('.')
        # 把句子长度小于4的剔除，一般这些都是转折等过渡语句，会干扰句子提取
        filter_index = [i for i in range(len(sentences)) if len(sentences[i]) >= 4]
        sentences = [sentences[i] for i in filter_index]
        flags = [flags[i] for i in filter_index]

        return sentences, flags

    # 用pyltp模型进行切句
    def __cut_sentence(self, string):
        """@string contain many sentence"""
        sents = SentenceSplitter.split(string)  # 分句
        sents = [sen for sen in sents if len(sen) > 4]
        return sents, None

    def __get_tokens(self, sentences):
        sen_tokens = []
        for i, sen in enumerate(sentences):
            sen_tokens.append([])
            words = jieba.cut(sen)
            for wp in words:
                if wp not in self.stopwords:
                    sen_tokens[i].append(wp)
        return sen_tokens

    # 获取文章主题
    # 可以根据文章主题和摘要主题进行相似度计算，如果相似度过低，
    # 可以重新调整各方面权重，重新提取摘要，单句进行主题对比LDA模型效果不好，词太少
    def __theme_re_weight(self, tokens):
        dictionary = Dictionary(tokens)
        corpus = [dictionary.doc2bow(text) for text in tokens]
        lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=2, passes=20)
        topic = []
        topic.append(lda.show_topic(topicid=0, topn=8))
        topic.append(lda.show_topic(topicid=1, topn=8))
        return topic

    def __knn_soft(self, sim):
        window = 2
        wight = np.array([0.1, 0.125, 0.5, 0.125, 0.1])
        sim = [sim[0]] * window + sim + [sim[-1]] * window
        sim = np.array(sim)
        sim = [np.dot(sim[i - window:i + window + 1], wight)
               for i in range(window, len(sim) - window)]
        return sim

    # 考虑标题的影响权重
    def __title_re_weight(self, sim, sim_title):
        sim = np.array(sim)
        sim_title = np.array(sim_title)
        p = 0.7
        sim = p * sim + (1 - p) * sim_title
        return list(sim)

    # 考虑关键字对摘要的影响权重
    def __keywords_re_weight(self, keywords, sim, tokens):
        for wp in keywords:
            for i, token in enumerate(tokens):
                if wp.word in token:
                    sim[i] = sim[i] + 0.02 * wp.weight  # 添加关键字的权重
        return sim

    # 考虑首位句子的影响权重
    def __startend_re_weight(self, sents, sim):
        if (len(sents[0]) > 20):
            sim[0] = sim[0] + 0.1
        return sim

    def get_summrazation(self, string, num, title=None):
        # sentences, flags = self.__split_sentence(string)
        sentences, flags = self.__cut_sentence(string)
        tokens = self.__get_tokens(sentences)
        tokens_all = reduce(operator.add, tokens)
        new_tokens = [tokens_all] + tokens
        sim = self.Sen_Embedding.get_similarity_result(self.model_wv, new_tokens)
        # test(sentences, sim)  # testpoint
        assert len(sim) == len(tokens)
        keywords = self.__get_keyword(string)
        # print(keywords)
        # 根据关键字重新更新一次权值
        sim = self.__keywords_re_weight(keywords, sim, tokens)
        # test(sentences, sim)  # testpoint
        # 如果有标题，则根据标题更新一次权值
        if title:
            title_tokens = self.__get_tokens([title])
            new_tokens = title_tokens + tokens
            sim_title = self.Sen_Embedding.get_similarity_result(self.model_wv, new_tokens)
            sim = self.__title_re_weight(sim, sim_title)

        # 根据首尾位置更新一次权值
        if self.position_re_weight:
            sim = self.__startend_re_weight(sentences, sim)
            # test(sentences, sim)  # testpoint

        sim = self.__knn_soft(sim)  ##knn soft
        # test(sentences, sim)  # testpoint

        assert len(sim) == len(tokens)
        index = list(np.argsort(sim))
        index = index[-num:]  ##取值最高的num项
        index.sort()  ##排序

        # 把标点也合并
        abstract = []
        if flags:
            for i in index:
                abstract.append(sentences[i])
                abstract.append(flags[i])
        else:
            abstract = [sentences[i] for i in index]

        topic = self.__theme_re_weight(tokens)

        keywords = [(wp.word, wp.weight) for wp in keywords]
        # for wp in keywords:
        #     result['keywords'].append({'cat': 'a', 'name': wp.word, 'value': 30, 'pro':wp.weight})

        return ''.join(abstract), keywords, topic


def data_format(abstract, keywords, topic):
    keywords = sorted(keywords, key=lambda x: x[1])
    length_range = keywords[-1][1]
    result = {}
    result['keywords'] = []
    for i, wp in enumerate(keywords):
        result['keywords'].append({'cat': i,
                                   'name': wp[0],
                                   'value': round(10 + 50 * wp[1] / length_range, 2),
                                   'pro': round(float(wp[1]), 4)})
    result['summarization'] = abstract
    topic_new = []
    for tp in topic:
        temp = []
        for wp in tp:
            temp.append({"name": wp[0], 'value': round(float(wp[1]), 4)})
        topic_new.append(temp)

    result['topics'] = topic_new
    return result


class My_Summrazation:
    # 外部接口类，把本文件功能全部集成在该类
    def __init__(self):
        self.Summ = Summarization()

    def get_results(self, text, num, title=None):
        # try:
        return data_format(*self.Summ.get_summrazation(text, num, title))
        # except:
        #     return None

    def release(self):
        del self.Summ.model_wv
        gc.collect()


if __name__ == "__main__":
    pass
