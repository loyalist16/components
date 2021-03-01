# -*- coding: utf-8 -*-
# @Time : 2021/2/23 11:00
# @Author : loyalist
# @Email : lzl0118@foxmail.com
# @File : ttf2img.py
# @Desc : 将ttf文件转为图片

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import numpy


def ttf2img(fontPath):
    """
    字体文件转换为图片
    :param str fontPath: 字体文件路径
    :return: 编码列表, 图片路径名字
    :rtype: tuple
    """
    im = Image.new('RGB', (1800, 1000), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(fontPath, 40)
    tt_font = TTFont(fontPath)
    code_list = tt_font.getGlyphOrder()[2:]
    array_list = numpy.array_split(code_list, 15)
    for i in range(15):
        newList = [j.replace("uni", "\\u") for j in array_list[i]]
        text = "".join(newList)
        text = text.encode('utf-8').decode('unicode_escape')
        dr.text((0, 50 * i), text, font=font, fill="#000000")
    font_imgName = "font.jpg"
    im.save(font_imgName)
    return code_list, font_imgName


if __name__ == '__main__':
    ttf2img('4165b8d8.woff')
