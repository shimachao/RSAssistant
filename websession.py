#-*-coding:UTF-8-*-
""" 访问RS网站
"""
import requests
from hashlib import md5
import parse


class RepeatSignError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TimeoutError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WebSession:
    """ 负责和rs网站的http交互
    """
    default_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 '
                                     'SE 2.X MetaSr 1.0',
                       'Origin': 'http://rs.xidian.edu.cn',
                       'Host': 'rs.xidian.edu.cn',
                       'Connection': 'keep-alive'}

    def __init__(self, username, password):
        self.s = requests.session()
        self.s.headers.update(WebSession.default_headers)
        self.username = username

        m = md5()
        m.update(password.encode('utf-8'))
        self.password = m.hexdigest()

    def login(self):
        url = 'http://rs.xidian.edu.cn/member.php'
        query_data = {'mod': 'logging',
                      'action': 'login',
                      'loginsubmit': 'yes',
                      'infloat': 'yes',
                      'lssubmit': 'yes',
                      'inajax': '1'}
        body_data = {'username': self.username,
                     'password': self.password,
                     'quickforward': 'yes',
                     'handlekey': 'ls'}
        headers = {'Cache-Control': 'max-age=0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Referer': 'http://rs.xidian.edu.cn/forum.php'}
        self.s.post(url=url, data=body_data, params=query_data, headers=headers)

    def turn_to_sign_page(self):
        """ 打开签到页面，并从返回的页面中得到一个form hash值，用于后面的签到操作
        """
        url = 'http://rs.xidian.edu.cn/plugin.php'
        query_data = {'id': 'dsu_paulsign:sign'}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Referer': 'http://rs.xidian.edu.cn/forum.php'}
        r = self.s.get(url=url, params=query_data, headers=headers)

        self.form_hash = parse.parse_out_form_hash(r.text)

    def sign(self):
        """ 签到
        """
        url = 'http://rs.xidian.edu.cn/plugin.php'
        query_data = {'id': 'dsu_paulsign:sign',
                      'operation': 'qiandao',
                      'infloat': '1',
                      'inajax': '1'}
        body_data = {'formhash': self.form_hash,
                     'qdxq': 'fd',
                     'qdmode': 2,
                     'todaysay': '',
                     'fastreply': 1}
        headers = {'Cache-Control': 'max-age=0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Referer': 'http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign',
                   'Proxy-Connection': 'keep-alive'}
        r = self.s.post(url=url, data=body_data, params=query_data, headers=headers)

        self.gold_num = parse.parse_out_gold_num(r.text)

    def get_gold_num(self):
        return self.gold_num

    def close(self):
        if self.s:
            self.s.close()
            self.s = None



if __name__ == '__main__':
    rs_web = WebSession(username='高手情结', password='531236305')

    rs_web.login()
    rs_web.turn_to_sign_page()
    rs_web.sign()
