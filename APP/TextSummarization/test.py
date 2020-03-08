#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：Valuebai
@Date   ：2019/11/15 17:27
@Desc   ：
=================================================='''
import pkuseg


'''
Title 标题
如果该文本有标题，那么标题可以帮助我们很多。
在之前，我们计算每个句子与文章整体的相似度是对每个子句与整体文章进行相似度距离计算，
那么，我们这个时候，就可以把标题的embedding结果拿出来，
那么每句话的相似度就是这句话与整体文章的相似度和标题的相似度的一个“结合”。
'''

title = 'some words'
content = 'more and more words'
sentene_vec_title = get_sentence_vec(title)
sentene_vec_content = get_sentence_vec(content)
#对于一个子句 sub_sen_n, 以前的similarity是 cosine(get_sentene_vec(sub_sen_n), sentene_vec_content)
#现在可以是
p = 0.5
sen_vec = get_sentene_vec(sub_sen_n)
similarity = p * cosine(sen_vec, sentene_vec_title) + (1 - p) * cosine(sen_vec, sentene_vec_content)
# 当然，这里的p以及p和cosine的构建都是可以变化的。 p 和 1-p是线性关系，可以是其他的关系。自己定即可

