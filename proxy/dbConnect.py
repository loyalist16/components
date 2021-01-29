# -*- coding: utf-8 -*-
# @Time : 2021/1/29 9:33
# @Author : loyalist
# @Email : lzl0118@foxmail.com
# @File : dbConnect.py
# @Desc : 连接各种数据库

import redis
import random
from proxy import setting


class MyRedisClient:
    """
    redis连接客户端
    """

    def __init__(self, host=setting.REDIS_HOST, port=setting.REDIS_PORT, passwd=setting.REDIS_PASSWORD,
                 proxy_key=setting.PROXY_KEY):
        """
        初始化redis连接
        :param str host: 主机
        :param str port: 端口
        :param str passwd: 密码
        :param str proxy_key: 哈希键名
        """
        self.db = redis.StrictRedis(host=host, port=port, password=passwd, decode_responses=True)
        self.proxy_key = proxy_key

    def set(self, name, proxy):
        """
        设置代理
        :param str name: 主机名称
        :param str proxy: 代理
        :return: 设置结果
        :rtype: int
        """
        return self.db.hset(self.proxy_key, name, proxy)

    def get(self, name):
        """
        获取代理
        :param str name: 主机名称
        :return: 代理
        :rtype: str
        """
        return self.db.hget(self.proxy_key, name)

    def count(self):
        """
        获取代理总数
        :return: 代理总数
        :rtype: int
        """
        return self.db.hlen(self.proxy_key)

    def remove(self, name):
        """
        删除代理
        :param str name: 主机名称
        :return: 删除结果
        :rtype: int
        """
        return self.db.hdel(self.proxy_key, name)

    def names(self):
        """
        获取主机名称列表
        :return: 名称列表
        :rtype: list
        """
        return self.db.hkeys(self.proxy_key)

    def proxies(self):
        """
        获取代理列表
        :return: 代理列表
        :rtype: list
        """
        return self.db.hvals(self.proxy_key)

    def random(self):
        """
        随机获取代理
        :return: 代理
        :rtype: str
        """
        proxies = self.proxies()
        return random.choice(proxies)

    def all(self):
        """
        获取所有 主机:代理 键值对
        :return: 所有代理
        :rtype: dict
        """
        return self.db.hgetall(self.proxy_key)


if __name__ == '__main__':
    rc = MyRedisClient()
    # p = rc.set('2', "153.35.238.242")
    p = rc.names()
    # p = rc.get('1')
    print(p, type(p))
