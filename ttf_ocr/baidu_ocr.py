# -*- coding: utf-8 -*-
# @Time : 2021/2/23 11:45
# @Author : loyalist
# @Email : lzl0118@foxmail.com
# @File : baidu_ocr.py
# @Desc : 百度的OCR项目

from aip import AipOcr

APP_ID = '**'
API_KEY = '**'
SECRET_KEY = '**'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def accurate_ocr(file):
    '''
    通用文字识别（高精度版）
    '''
    """ 读取图片 """

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(file)

    """ 调用通用文字识别（高精度版） """
    result = client.basicAccurate(image)
    return result

