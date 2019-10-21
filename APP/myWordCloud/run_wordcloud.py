#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/10/18 16:52
@Desc   ： 绘制图云

【经验】不要在函数中写死路径，将路径写成参数，在使用的main 中调用

注意：
@ 本代码使用的是处理过的单词
词云使用的是{'string': weight_int, ... , 'string': weight_int}
用wc.generate_from_frequencies(word_cloud)来生成
    
@ 使用的是文本的话，需要结合jieba分词使用
text = ''''''疾风剑豪·亚索是网络竞技游戏《英雄联盟》里面第117位英......''''''
cut_text = ' '.join(jieba.lcut(text))
word_cloud = wc.generate(cut_text)
=================================================='''
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os


def get_mask():
    '''
    获取一个圆形的mask，画图时使用这个圆形作为背景图
    :return 'numpy.ndarray'
    '''
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    return mask


def get_heart_mask():
    """
    画一个心型图并展示，其他地方未使用到
    :return:
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # plt.title('heart', fontsize=24)#图名
    x = np.linspace(-1, 1, 300)
    # 把函数分为上下两个部分
    y1 = np.sqrt(1 - np.power(x, 2)) + np.power(np.square(x), 0.33)
    y2 = -np.sqrt(1 - np.power(x, 2)) + np.power(np.square(x), 0.33)
    # 设置一下x轴、y轴的刻度和坐标间距，为了显示结果的美观，在此取消坐标轴
    # my_x_ticks = np.arange(-2, 2.5, 0.5)
    # my_y_ticks = np.arange(-2, 2.5, 0.5)
    plt.plot(x, y1, color='r')  # 绘制心形上方部分
    plt.plot(x, y2, color='r')  # 绘制下半部分
    plt.fill_between(x, y1, y2, where=y1 >= y2, facecolor='red', interpolate=True)  # 染色
    # plt.xticks(my_x_ticks)#坐标刻度
    # plt.yticks(my_y_ticks)
    plt.axis('off')  # 取消显示坐标轴
    plt.show()


def draw_word_cloud(word_cloud, DIR_font, DIR_image, DIR_Save_Image):
    '''
    绘制词云，需要添加.ttf字体，否则会显示乱码的
    .ttf文件在windows里面直接搜索即可
    word_cloud: 约定输入的格式为：{'string': weight_int, ... , 'string': weight_int}
    DIR_font: 加载字体的路径，在使用的.py中定义
    DIR_image: 加载背景图片的路径，在使用的.py中定义

    :return: None
    '''

    # 设置停用词
    stopword = ("这个不生效，后面再看下", "慈爱")  # Ignored if using generate_from_frequencies.
    # 打开一张图片，词语以图片形状为背景分布
    background_Image = np.array(Image.open(DIR_image))

    wc = WordCloud(
        # wordcloud参数配置
        background_color="white",  # 背景颜色
        mask=background_Image,  # 背景图片1.from PIL import Image 2.hand = np.array(Image.open('hang1.jpg')) # 词语以图片形状为背景分布
        # mask=get_mask(), # 使用上面的圆圈/心型的mask
        max_words=2000,  # 最大显示的字数
        margin=2,  # 页面边缘
        scale=2,  # 尺寸比例，默认600x800, =2,1200x1600，用这个就不用看Width/height of the canvas
        # stopwords=stopword,  # 停用词，Ignored if using generate_from_frequencies.
        font_path=DIR_font,  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_font_size=100,  # 字体最大值
        random_state=42,  # 设置有多少种随机生成状态，即有多少种配色方案
    )
    # 生成图云
    wc.generate_from_frequencies(word_cloud)

    ## 生成的图片，颜色是随机的
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")  # 隐藏x轴和y轴
    plt.figure()
    wc.to_file(DIR_Save_Image + r'RandomColor.png')  # 保存图片，只保存1张的

    ## 生成的图片，颜色是设置为背景色
    # 提取背景图片颜色
    img_colors = ImageColorGenerator(background_Image)
    plt.imshow(wc.recolor(color_func=img_colors), interpolation="bilinear")
    plt.axis("off")  # 隐藏x轴和y轴
    plt.figure()
    wc.to_file(DIR_Save_Image + r'BGColor.png')  # 保存图片，只保存1张的

    ## 显示设置的背景图片
    plt.imshow(background_Image, cmap=plt.cm.gray, interpolation="bilinear")
    plt.axis("off")  # 隐藏x轴和y轴

    # 讲图片在pycharm中显示出来
    plt.show()


def run_draw(word, DIR_font, DIR_image, DIR_Save_Image):
    '''
    测试绘制的词云
    word: # 约定输入的格式： [('string', weight_int), ... ,('string', weight_int)]
    DIR_font: 加载字体的路径，在使用的.py中定义
    DIR_image: 加载背景图片的路径，在使用的.py中定义

    :return: 显示画的图
    '''

    # 将返回的结果转换为字典,便于绘制词云
    word_cloud = dict()
    for sim in word:
        # print(sim[0],":",sim[1])
        word_cloud[sim[0]] = sim[1]
    # print(word_cloud)
    # 绘制词云
    draw_word_cloud(word_cloud, DIR_font, DIR_image, DIR_Save_Image)


if __name__ == "__main__":
    # # 输入一个词找出相似的前100个词
    # result = model.wv.most_similar(word, topn=100)
    # 约定输入的格式： [('string', weight_int), ... ,('string', weight_int)]
    word = [('慈爱', 0.9991910457611084), ('寻求', 0.9990566968917847), ('举手', 0.9983204007148743),
            ('之神', 0.9979360103607178), ('垂顾', 0.9979304075241089), ('呼求', 0.9977825880050659),
            ('大能者', 0.9976420998573303), ('赐福', 0.997443675994873), ('求告', 0.9971387386322021),
            ('好事', 0.99695885181427), ('主', 0.994560182094574), ('耶和华', 0.993634819984436), ('万军', 0.9923015832901001),
            ('论摩押', 0.9767180681228638), ('扫罗之手', 0.9765521883964539), ('看为', 0.973850429058075),
            ('性爱', 0.9723807573318481), ('名', 0.9718977212905884), ('你祖', 0.9710243940353394),
            ('求', 0.9705307483673096), ('拔营', 0.9977777600288391), ('约翰', 0.9976563453674316),
            ('西拿基立', 0.9974972009658813), ('逃往', 0.9973836541175842), ('沙基', 0.9971573948860168),
            ('巴沙', 0.9971001148223877), ('书念', 0.9970910549163818), ('请', 0.9969766139984131),
            ('耶弗', 0.9968913793563843), ('聚集', 0.9968770742416382)]

    # 定义字体，背景图片的路径
    DIR_font = os.path.join(os.path.abspath('../..'), r'data\ping.ttf')
    DIR_image = os.path.join(os.path.abspath('../..'), r'data\alice.png')
    DIR_Save_Image = os.path.join(os.path.abspath('../..'), r'data\saveWordCould')

    run_draw(word, DIR_font, DIR_image, DIR_Save_Image)

    # 测试mask
    # get_mask()
    # get_heart_mask()
