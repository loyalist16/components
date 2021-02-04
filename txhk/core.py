# -*- coding: utf-8 -*-
# @Time : 2021/2/3 13:33
# @Author : loyalist
# @Email : lzl0118@foxmail.com
# @File : core.py
# @Desc : 腾讯滑块破解
import base64
import requests
import re
import time
import warnings
from urllib.parse import quote

warnings.filterwarnings('ignore')


class Txhk:
    def __init__(self, ua, aid, refer_url):
        self._ua = ua
        self.aid = aid
        self.refer_url = refer_url

    @property
    def ua(self):
        return base64.b64encode(self._ua.encode()).decode()

    def initCaptcha(self):
        """
        初始化验证 获取sess, sid
        :param str aid: 用户id
        :param str ua: ua
        :return: 结果
        :rtype: dict
        """
        url = "https://t.captcha.qq.com/cap_union_prehandle"
        params = {
            'aid': self.aid, 'protocol': 'https', 'accver': '1', 'showtype': 'popup',
            'ua': self.ua,
            'noheader': '1', 'fb': '1', 'enableDarkMode': '0', 'grayscale': '1', 'clientype': '2',
            'lang': 'zh-CN',
            'subsid': '1', 'callback': '_aq_716998'
        }
        headers = {
            'Host': 't.captcha.qq.com',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self._ua,
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            'Referer': self.refer_url,  # 根据不同程序改变
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }

        response = requests.get(url, headers=headers, params=params, verify=False)
        s = re.search('_aq_716998\((.*)\)', response.text).group(1)
        result = eval(s)
        # {"state":1,"ticket":"","capclass":"1","subcapclass":"15","src_1":"cap_union_new_show","src_2":"template/new_placeholder.html","src_3":"template/new_slide_placeholder.html","sess":"s0On0zvlytShIM4z6GoUJV5m0WYGy0Dj1O4bOxPpmlARN9P7uJNkP5UADIPDMQtEcA3uwzHdf_zq9Z4BSw8tM3NTTM9H5lA1MTdRSrbfCNsUx5rKJak4b2Zorv1zVNQZfwkEbTcSwuoEjzIFvyjZ0K_yjVY0YwceLjkN4O0SierPzIJ-BWI0uaWxoWCv1dY7w0E8cnx24D1Ek*","randstr":"","sid":"6762554139436920832"}
        return result

    def showCaptcha(self, sess, sid):
        """
        验证码显示页面, 获取验证码id
        :param str sess: initCaptcha 生成
        :param str sid: initCaptcha 生成
        :return: 验证码id, 请求url, nonce
        :rtype: (str, str, str)
        """
        self.rnd = '535739'
        self.createIframeStart = f'{int(time.time() * 1000)}'
        self.prehandleLoadTime = '273'
        url = "https://t.captcha.qq.com/cap_union_new_show"
        params = {
            'aid': self.aid, 'protocol': 'https', 'accver': '1', 'showtype': 'popup',
            'ua': self.ua,
            'noheader': '1', 'fb': '1', 'enableDarkMode': '0', 'grayscale': '1', 'clientype': '2',
            'sess': sess,
            'fwidth': '0', 'sid': sid, 'forcestyle': 'undefined', 'tcScale': '1',
            'rnd': self.rnd,
            'TCapIframeLoadTime': 'undefined',
            'prehandleLoadTime': self.prehandleLoadTime,
            'createIframeStart': self.createIframeStart,
            'subsid': '2'
        }
        headers = {
            'Host': 't.captcha.qq.com',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self._ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': self.refer_url,
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }

        response = requests.get(url, headers=headers, params=params, verify=False)
        img_id = re.search('image=(\d+)?', response.text).group(1)
        nonce = re.search('nonce:"(.*?)"', response.text).group(1)
        eks_url = re.search('dcFileName:"(.*?)"', response.text).group(1)
        return img_id, response.request.url, nonce, eks_url

    def resetSess(self, sess, sid, show_url):
        """
        重置sess, 并获取初始滑动位置
        :param str sess: initCaptcha 生成
        :param str sid: initCaptcha 生成
        :param str show_url: 验证码显示页面url
        :return: 结果
        :rtype: dict
        """
        url = "https://t.captcha.qq.com/cap_union_new_getsig"

        payload = f"aid={self.aid}&protocol=https&accver=1&showtype=popup&ua={quote(self.ua)}" \
                  f"&noheader=1&fb=1&enableDarkMode=0&grayscale=1&clientype=2&sess={sess}&fwidth=0&sid={sid}&forcestyle=undefined" \
                  f"&wxLang=&tcScale=1&uid=&cap_cd=&rnd={self.rnd}&TCapIframeLoadTime=undefined&prehandleLoadTime={self.prehandleLoadTime}&" \
                  f"createIframeStart={self.createIframeStart}&subsid=2&rand=99947704"
        headers = {
            'Host': 't.captcha.qq.com',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self._ua,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://t.captcha.qq.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': show_url,
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        # {'ret': '0', 'sess': 's0RtRP3ArZ4B7NVpRRZnCjofZ7RDj0qBLHRme1xLyGllMt5ElSEollN9UD41KZcP9fdtyVDWfuUeXpyyJ14kI0g55UPi9srdReuc9GOFWwe4EvAwJtMoe_jwi2-81TEelOA3ERgbepgmobOrK-ckUaQUcNP5EeC0Gcj51wTN2BfPDikyvKdQtjNRKKUS4Exfjb7ojieTJsBb6YUZXYhI7R4_vfU8ejqRFpdQbMA8pIIbY*', 'cdnPic1': '/hycdn?index=1&image=937032639779710976', 'cdnPic2': '/hycdn?index=2&image=937032639779710976', 'initx': '68', 'inity': '66'}
        return response.json()

    def loadImage(self, sess, sid, show_url):
        """
        下载验证码图片
        :param sess: resetSess生成
        :param sid: initCaptcha生成
        :param referer: 验证码显示页面url
        :return: None
        """
        # 缺口图片
        url1 = f"https://t.captcha.qq.com/cap_union_new_getcapbysig?aid={self.aid}&" \
               f"sess={sess}&sid={sid}&img_index=1&subsid=7"
        headers = {
            'Host': 't.captcha.qq.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self._ua,
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'image',
            'Referer': show_url,
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }
        response = requests.request("GET", url1, headers=headers, verify=False)
        with open('topic7_1.png', 'wb') as f:
            f.write(response.content)

        # 小图片
        url2 = f"https://t.captcha.qq.com/cap_union_new_getcapbysig?aid={self.aid}&" \
               f"sess={sess}&sid={sid}&img_index=2&subsid=8"
        response = requests.request("GET", url2, headers=headers, verify=False)
        with open('topic7_2.png', 'wb') as f:
            f.write(response.content)

        # 完整图片
        url3 = f"https://t.captcha.qq.com/cap_union_new_getcapbysig?aid={self.aid}&" \
               f"sess={sess}&sid={sid}&img_index=0&subsid=9"
        response = requests.request("GET", url3, headers=headers, verify=False)
        with open('topic7_0.png', 'wb') as f:
            f.write(response.content)

    def get_eks(self, eks_url, show_url):
        url = "https://t.captcha.qq.com/" + eks_url

        payload = {}
        headers = {
            'Host': 't.captcha.qq.com',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self._ua,
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            'Referer': show_url,
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        eks = re.search('\.info="(.*?)"', response.text).group(1)
        print(eks)

    def verify(self, sess, sid, nonce, eks, show_url, ans):
        url = "https://t.captcha.qq.com/cap_union_new_verify"
        payload = {
            'aid': self.aid, 'protocol': 'https', 'accver': '1', 'showtype': 'popup',
            'ua': self.ua,
            'noheader': '1', 'fb': '1', 'enableDarkMode': '0', 'grayscale': '1', 'clientype': '2',
            'sess': sess,
            'fwidth': '0',
            'sid': sid, 'forcestyle': 'undefined', 'wxLang': '', 'tcScale': '1', 'uid': '', 'cap_cd': '',
            'rnd': self.rnd, 'TCapIframeLoadTime': 'undefined', 'prehandleLoadTime': self.prehandleLoadTime,
            'createIframeStart': self.createIframeStart, 'subsid': '2', 'cdata': '0',
            'ans': ans,  # '320,107;'
            'collect': collect,
            'vsig': '', 'websig': '', 'subcapclass': '',
            'tlg': len(collect),
            'eks': eks,
            'nonce': nonce, 'vlg': '0_0_1',
            'vData': vData
        }
        headers = {
            'Host': 't.captcha.qq.com',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self._ua,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://t.captcha.qq.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': show_url,
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }

        response = requests.request("POST", url, headers=headers, data=payload)


if __name__ == '__main__':
    tx = Txhk(
        ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        aid="2005597573",
        refer_url="http://www.glidedsky.com/"
    )
    tx.initCaptcha()
    init_obj = tx.initCaptcha()
    print(init_obj, type(init_obj))
    sess = init_obj['sess']
    sid = init_obj['sid']
    r = tx.showCaptcha(sess, sid)
    print(r)
    eks = tx.get_eks(r[3], r[1])
