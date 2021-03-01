# -*- coding: utf-8 -*-
# @Time : 2021/3/1 17:35
# @Author : loyalist
# @Email : lzl0118@foxmail.com
# @File : run.py
# @Desc : 识别图片中的文字

from baidu_ocr import accurate_ocr
from ttf2img import ttf2img
from loguru import logger


def get_fontMap(fontPath):
    """
    获取 编码:字符 映射表
    :param str fontPath: 字体文件路径
    :return: 字体映射 或者 ocr识别有缺漏,则返回code_list和识别后的字体列表, 核实完后手动dict(zip())生成映射
    :rtype: dict|tuple
    """
    code_list, img_name = ttf2img(fontPath=fontPath)
    result = accurate_ocr(img_name)
    print(result)
    words_result = [words.get('words') for words in result.get('words_result')]
    words = ''.join(words_result)
    words_list = list(words)
    if len(words_list) == len(code_list):
        font_map = dict(zip(code_list, words_list))
        print(font_map)
        return font_map
    else:
        error_words = min(words_result, key=len)
        line = words_result.index(error_words) + 1
        logger.error("第{}行, 字体有缺漏, 请核对 `{}` ", line, error_words)
        return code_list, words_list


if __name__ == '__main__':
    get_fontMap('4165b8d8.woff')
