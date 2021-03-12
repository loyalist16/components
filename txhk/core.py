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
import execjs
from urllib.parse import quote
from txhk.gap import get_left_offset
from PIL import Image

warnings.filterwarnings('ignore')


class Txhk:
    def __init__(self, ua, aid, refer_url, app_version):
        """
        初始化
        :param ua: User-Agent
        :param aid: 滑块使用者aid
        :param refer_url: 来源url
        :param app_version: navigator.appVersion值
        """
        self._ua = ua
        self.aid = aid
        self.refer_url = refer_url
        self.app_version = app_version

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
        :return: 请求url, nonce, tdc_url
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
        # img_id = re.search('image=(\d+)?', response.text).group(1)
        nonce = re.search('nonce:"(.*?)"', response.text).group(1)
        tdc_url = re.search('dcFileName:"(.*?)"', response.text).group(1)
        return response.request.url, nonce, tdc_url

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

    def get_tdc_js(self, tdc_url, show_url):
        """
        获取到tdc_js文件
        :param str tdc_url: tdc文件url
        :param show_url: 验证码展示窗口url
        :return: tdc_js文件内容
        :rtype: str
        """
        url = "https://t.captcha.qq.com/" + tdc_url

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
        return response.text

    def get_collect(self, tdc, location_href, start_pos, end_pos):
        """
        获取加密参数collect
        :param str tdc: 动态tdc文件
        :param str location_href: 验证码的展示链接
        :param list start_pos: 滑块开始滑动坐标
        :param list end_pos: 滑块结束滑动坐标
        :return: collect参数
        :rtype: str
        """
        jscode = """const {JSDOM} = require('jsdom');

// 重写require库, 过fs检测
var ori_require = require;
require = function (v) {
  console.log("重写require", v);
  if (v === 'fs') {
    return false;
  } else {
    return ori_require(v);
  }
}
"""
        jscode += "const dom = new JSDOM('', {url: '%s',referrer: '%s',contentType: 'text/html',includeNodeLocations: true,storageQuota: 10000000})" % (
            location_href, self.refer_url)
        jscode += """
// 加载
dom.window.dispatchEvent(new dom.window.Event('load'));
// window设为全局
var window = global;
delete process.cwd;;
window.addEventListener = function (event, callback, flag) {
  dom.window.addEventListener(event, callback, flag);
}
window.location = dom.window.location;
window.WebGLRenderingContext = function () {
}
WebGLRenderingContext.toString = function () {
  return "function WebGLRenderingContext() { [native code] }";
}

document = dom.window.document;
"""
        jscode += """// navigator
navigator = dom.window.navigator;
Object.defineProperties(navigator, {
  appVersion: {value: "%s"},
  platform: {value: "Win32"},
  languages: {value: ["zh-CN", "zh-TW", "zh", "en-US", "en"]},
  userAgent: {value: "%s"},
  plugins: {value: [{name: "Chrome PDF Plugin"}, {name: "Chrome PDF Plugin"}, {name: "Chrome PDF Viewer"}]},
})
""" % (self.app_version, self._ua)
        jscode += """navigator.getBattery = function () {
  let num = 0.6;
  return new Promise((resolve, reject) => {
  })
}
// plugins: [{name: "Chrome PDF Plugin"}, {name: "Chrome PDF Plugin"}, {name: "Chrome PDF Viewer"}],
window.innerWidth = 360;
window.innerHeight = 360;
screen = dom.window.screen;
Object.defineProperties(screen, {
  availHeight: {value: 1040},
  availLeft: {value: 1920},
  availTop: {value: 0},
  availWidth: {value: 1920},
  colorDepth: {value: 24},
  height: {value: 1080},
  pixelDepth: {value: 24},
  width: {value: 1920},
  orientation: {
    value: {
      angle: 0,
      onchange: null,
      type: "landscape-primary"
    }
  }
})

// canvas
dom.window.HTMLCanvasElement.prototype.toDataURL = function () {
  return "data:image/png;base64,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"
}
dom.window.HTMLCanvasElement.prototype.getContext = function (v) {
  if (v === '2d') {
    return {
      isPointInPath: function (args) {
        return false
      },
      rect: function (args) {
      },
      fillRect: function (args) {
      },
      fillText: function (args) {
      },
      beginPath: function () {
      },
      arc: function (args) {
      },
      closePath: function () {
      },
      fill: function () {
      }
    };
  } else {
    return {
      getExtension: function (args) {
        return {
          UNMASKED_RENDERER_WEBGL: 1
        }
      },
      getParameter: function (args) {
        return "ANGLE(Intel(R)UHDGraphics630Direct3D11vs_5_0ps_5_0)"
      }
    };
  }
}

// 监听事件
var md = new dom.window.Event('mousedown');
var mu = new dom.window.Event('mouseup');
var cl = new dom.window.Event('click');
var mv = new dom.window.Event('mousemove');

// 轨迹函数
function track(start_pos, end_pos) {
  /* start_pos 点击的坐标
  * end_pos 结束的坐标
  * */
  const distance = end_pos[0];
  let click_pos = start_pos[0];
  let a = 0.00035, // 加速度
    current = 0, //当前位移
    t = 0.02, //计算间隔
    v = 0, //初速度
    mid = distance * 4 / 5; // 减速阈值
  while (current < distance) {
    v0 = v; //初速度v0
    v = v0 + a * t; //当前速度
    move = v0 * t + 1 / 2 * a * t * t; // 移动距离
    // console.log("每次移动: ", move)
    if (parseInt(move) > 0) {
      current += parseInt(move); //当前位移
      if (current < mid) {
        if (current % (parseInt(Math.random() * 5)) == 0) {
          mv.pageX = current;
          mv.pageY = start_pos[1];
          document.dispatchEvent(mv);
        }
        if (current >= click_pos) {
          md.pageX = current;
          md.pageY = start_pos[1];
          document.dispatchEvent(md);
          click_pos += 9999;
        }
      } else {
        mv.pageX = current;
        mv.pageY = start_pos[1];
        document.dispatchEvent(mv);
        if (current == end_pos[0]) {
          mu.pageX = cl.pageX = current;
          mu.pageY = cl.pageY = start_pos[1];
          document.dispatchEvent(mv);
          document.dispatchEvent(cl);
        }
      }
    }
  }
}
        """
        jscode += tdc
        jscode += """function run(start_pos, end_pos) {
  track(start_pos, end_pos);
  collect = window.TDC.getData(!0);
  return decodeURIComponent(collect);
}
        """
        ctx = execjs.compile(jscode)
        collect = ctx.call('run', start_pos, end_pos)
        return collect

    def verify(self, sess, sid, nonce, eks, show_url, ans, collect):
        """
        滑块验证码验证
        :param str ssess: resetSess生成
        :param str sid: initCaptcha生成
        :param str nonce: showCaptcha生成
        :param str eks: tdc文件中动态变量
        :param str show_url: 验证码展示url
        :param str sans: 验证码终点坐标 格式: 'x,y;'
        :param str collect: 环境检测后的加密参数
        :return: 验证结果,errorCode为0表示成功
        :rtype: dict
        """
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
            'nonce': nonce, 'vlg': '0_0_1'
            # 'vData': vData
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
        return response.json()


def run(tx):
    """
    执行函数
    :param tx: Txhk对象
    :return: 验证结果
    """
    # 初始化滑块
    init_obj = tx.initCaptcha()
    sess = init_obj['sess']
    sid = init_obj['sid']
    # 获取验证码url, nonce, tdc文件url
    location_href, nonce, tdc_url = tx.showCaptcha(sess, sid)
    # 重置sess获取缺口初始位置
    r = tx.resetSess(sess, sid, location_href)
    sess = r.get('sess')
    # 下载图片并获取缺口左边位置
    tx.loadImage(sess, sid, location_href)
    img1 = Image.open('topic7_0.png').convert('RGBA')
    img2 = Image.open('topic7_1.png').convert('RGBA')
    left_offset = get_left_offset(img1, img2)
    ans = f"{left_offset - 20},{r.get('inity')};"  # 20是小图片左边距
    print(ans)
    # 起点坐标
    start_pos = [68, 285]
    # 终点坐标
    end_pos = [(left_offset + 44) // 2 + 12, 285]  # 44是小图片宽度, 12是图片距窗口左边距离
    # 获取tdc文件
    tdc = tx.get_tdc_js(tdc_url=tdc_url, show_url=location_href)
    tdc = tdc.replace('=254;', '=200;').replace('+=5293}', '+=0}')  # 将检测电源值转为200, 以及是否有process函数改为0
    eks = re.search('\.info="(.*?)"', tdc).group(1)
    # 执行js, 获取collect加密参数
    collect = tx.get_collect(tdc=tdc, location_href=location_href, start_pos=start_pos, end_pos=end_pos)
    result = tx.verify(sess=sess, sid=sid, nonce=nonce, eks=eks, show_url=location_href, ans=ans, collect=collect)
    return result


if __name__ == '__main__':
    tx = Txhk(
        ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        aid="2005597573",
        refer_url="http://www.glidedsky.com/",
        app_version="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    )
    result = run(tx)
    print(result)
