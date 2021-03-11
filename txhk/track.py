# -*- coding: utf-8 -*-
# @Time : 2021/3/11 16:22
# @Author : loyalist
# @Email : lzl0118@foxmail.com
# @File : track.py
# @Desc : 获取到缺口所在位置, 伪造轨迹

from PIL import Image


def get_pixel_list(file_path):
    """
    获取图片像素列表
    :param file_path: 文件路径
    :return: 图片像素列表
    """
    img = Image.open(file_path)
    img = img.convert('RGBA')
    return img.load()


def is_pixel_equal(img1_list, img2_list, x, y):
    """
    判断两张图相同坐标处像素是否相同
    :param PixelAccess img1: 图片1的像素列表
    :param PixelAccess img2: 图片2的像素列表
    :param int x: 横坐标
    :param int y: 纵坐标
    :return: bool
    :rtype: bool
    """
    pixel1 = img1_list[x, y]
    pixel2 = img2_list[x, y]
    threshold = 45
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        return False

def get_left_offset(img1, img2):
    """
    获取图片左边偏移量
    :param img1: 全图
    :param img2: 缺口图
    :return: 缺口左边距离
    """
    left = 60
    top = 30
    img1_list = img1.load()
    img2_list = img2.load()
    for x in range(left, img1.size[0]):
        for y in range(top, img1.size[1]):
            if not is_pixel_equal(img1_list, img2_list, x, y):
                left = x
                return left

if __name__ == '__main__':
    img1 = Image.open('topic7_0.png').convert('RGBA')
    img2 = Image.open('topic7_1.png').convert('RGBA')
    left = get_left_offset(img1, img2)
    print(left)