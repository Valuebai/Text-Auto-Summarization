#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/14 10:55
@Desc   ：用textrank4zh实现自动摘要, 基于PageRank改进的TextRank算法。

textrank4zh提取关键的效果比jieba的好太多了

注意：
- python中创建的packages/.py的名字不能跟pip install 的名字一样，不然在路径寻找中会优先找本项目中的packages名字，
  再去找lib下的，如：一开始将textran4zh-run命名为textrank4zh，就会出现报警，说找不到Text4Keyword
- .py文件命名时不要使用-，不然from import时识别不出来

- 在目录下执行python textrank4zh.py
- 报错 ModuleNotFoundError: No module named 'conf'
- 原因：https://stackoverflow.com/questions/52557522/modulenotfounderror-no-module-named-xxx-conf-xxx-is-not-a-package

- 解决方法：在代码最上面中添加
import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_dir)[0]
sys.path.append(rootPath)
=================================================='''
from textrank4zh import TextRank4Keyword, TextRank4Sentence, Segmentation
import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_dir)[0]
sys.path.append(rootPath)


# from conf import GetConfParams
#
# logger = GetConfParams().logger


def get_textrank4zh_keywords(contents):
    """
    获取文本关键字
    :param contents: string
    :return: dict of list [{x},{x}]
    """
    # 定义返回前10个关键词
    topK = 10
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=contents, lower=True)

    # logger.info('使用textrank4zh提取关键词，默认提取10个')
    # print('摘要：')
    # for item in tr4w.get_keywords(10, word_min_len=1):
    #     print(item.word, item.weight)
    result_topK = tr4w.get_keywords(topK, word_min_len=1)

    result = []
    # 封装成指定字典格式
    for i, wp in enumerate(result_topK):
        result.append({
            'cat': i,
            'word': wp['word'],  # 关键字
            'weight': round(wp['weight'], 4),  # 权值
            'value': round(wp['weight'] * 10000, 2)  # 用户画图用的，想办法权值差异化更加明显，画图更有区分
        })

    return result


def get_textrank4zh_keywords_phrase(contents):
    """
    获取文本关键字短语，这个功能有点不完善，不好用
    :param contents: string
    :return: dict of list [{x},{x}]
    """
    # 定义返回前20个关键词短语
    topK = 20
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=contents, lower=True)

    # logger.info('使用textrank4zh提取关键词短语，默认提取20个')

    # print('关键短语：')
    # for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
    #     print(phrase)

    result = tr4w.get_keyphrases(keywords_num=topK, min_occur_num=2)

    return result


def get_textrank4zh_summarization(contents):
    """
    获取文本摘要
    :param contents: string
    :return: dict of list [{x},{x}]
    """
    # 定义返回前5个文本摘要
    topK = 5
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=contents, lower=True, source='all_filters')

    # logger.info('使用textrank4zh提取摘要，默认提取5个')

    # print('摘要：')
    # for item in tr4s.get_key_sentences(num=5):
    #     print('文本位置：{}, 权重：{}，内容：{}'.format(item.index, item.weight, item.sentence))  # index是语句在文本中位置，weight是权重

    result = tr4s.get_key_sentences(num=topK)

    return result


def get_textrank4zh_summarization_str(contents):
    """
    获取文本摘要，返回的是string
    :param contents: string
    :return: string
    """
    # 定义返回前5个文本摘要
    topK = 5
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=contents, lower=True, source='all_filters')

    # logger.info('使用textrank4zh提取摘要，默认提取5个')

    # print('摘要：')
    # for item in tr4s.get_key_sentences(num=5):
    #     print('文本位置：{}, 权重：{}，内容：{}'.format(item.index, item.weight, item.sentence))  # index是语句在文本中位置，weight是权重

    result_topK = tr4s.get_key_sentences(num=topK)

    temp = []
    for item in result_topK:
        sent = item['sentence']
        temp.append(sent)

    return ''.join(temp)


if __name__ == "__main__":
    text = """
    中新网北京12月1日电(记者 张曦) 30日晚，高圆圆和赵又廷在京举行答谢宴，诸多明星现身捧场，其中包括张杰(微博)、谢娜(微博)夫妇、何炅(微博)、蔡康永(微博)、徐克、张凯丽、黄轩(微博)等。

30日中午，有媒体曝光高圆圆和赵又廷现身台北桃园机场的照片，照片中两人小动作不断，尽显恩爱。事实上，夫妻俩此行是回女方老家北京举办答谢宴。

群星捧场 谢娜张杰亮相

当晚不到7点，两人十指紧扣率先抵达酒店。这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。

高圆圆身穿粉色外套，看到大批记者在场露出娇羞神色，赵又廷则戴着鸭舌帽，十分淡定，两人快步走进电梯，未接受媒体采访。

随后，谢娜、何炅也一前一后到场庆贺，并对一对新人表示恭喜。接着蔡康永满脸笑容现身，他直言：“我没有参加台湾婚礼，所以这次觉得蛮开心。”

曾与赵又廷合作《狄仁杰之神都龙王》的导演徐克则携女助理亮相，面对媒体的长枪短炮，他只大呼“恭喜！恭喜！”

作为高圆圆的好友，黄轩虽然拍杂志收工较晚，但也赶过来参加答谢宴。问到给新人带什么礼物，他大方拉开外套，展示藏在包里厚厚的红包，并笑言：“封红包吧！”但不愿透露具体数额。

值得一提的是，当晚10点，张杰压轴抵达酒店，他戴着黑色口罩，透露因刚下飞机所以未和妻子谢娜同行。虽然他没有接受采访，但在进电梯后大方向媒体挥手致意。

《我们结婚吧》主创捧场

黄海波(微博)获释仍未出席

在电视剧《咱们结婚吧》里，饰演高圆圆母亲的张凯丽，当晚身穿黄色大衣出席，但只待了一个小时就匆忙离去。

同样有份参演该剧，并扮演高圆圆男闺蜜的大左(微信号：dazuozone) 也到场助阵，28日，他已在台湾参加两人的盛大婚礼。大左30日晚接受采访时直言当时场面感人，“每个人都哭得稀里哗啦，晚上是吴宗宪(微博)(微信号：wushowzongxian) 主持，现场欢声笑语，讲了好多不能播的事，新人都非常开心”。

最令人关注的是在这部剧里和高圆圆出演夫妻的黄海波。巧合的是，他刚好于30日收容教育期满，解除收容教育。

答谢宴细节

宾客近百人，获赠礼物

记者了解到，出席高圆圆、赵又廷答谢宴的宾客近百人，其中不少都是女方的高中同学。

答谢宴位于酒店地下一层，现场安保森严，大批媒体只好在酒店大堂等待。期间有工作人员上来送上喜糖，代两位新人向媒体问好。

记者注意到，虽然答谢宴于晚上8点开始，但从9点开始就陆续有宾客离开，每个宾客都手持礼物，有宾客大方展示礼盒，只见礼盒上印有两只正在接吻的烫金兔子，不过工作人员迅速赶来，拒绝宾客继续展示。

    """
    text2 = """
    王靖清说他是一个很好看的人，林诗宁表示她也是这么想的。是真的。
    
    """
    keyWords = get_textrank4zh_keywords(text)
    print('获取关键词：', keyWords)
    keyWords_phrase = get_textrank4zh_keywords_phrase(text)
    print('获取关键短语：', keyWords_phrase)

    extract = get_textrank4zh_summarization(text)
    print('获取摘要：', extract)

    extract_str = get_textrank4zh_summarization_str(text)
    print('获取摘要sting：', extract_str)
