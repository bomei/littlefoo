import json
import os

import requests
import tornado.web
from bs4 import BeautifulSoup

from pingjiao.pingjiao import Pingjiao


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

    def get_current_xsrf(self):
        return self.get_secure_cookie('_xsrf')

    @staticmethod
    async def db_login(c, db, username, pwd):
        await c[db].authenticate(username, pwd)


class IndexHandler(BaseHandler):
    def get(self):
        self.render('LT_bootstrap.html')


class DictHandler(BaseHandler):
    @staticmethod
    def gen_url(word):
        return 'http://cn.bing.com/dict/search?q={}&go=%E6%90%9C%E7%B4%A2&qs=n&form=Z9LH5&sp=-1&pq={}&sc=8-5&sk=&cvid=1026B339A8EA48DEA3EC59C4B2CFCD14'.format(
            word, word)

    def get(self):
        self.render('dict_bootstrap.html')

    def post(self):
        word = self.get_argument('word', None)
        if word is not None:
            bs = BeautifulSoup(requests.get(self.gen_url(word)).text)
            res = bs.find_all(attrs={'class': 'def_pa'})
            print(1)
            self.write(json.dumps({'1': [str(each) for each in res]}))


class QRCodeHandler(BaseHandler):
    def get(self):
        self.render('solve_qrcode.html')

    async def post(self, *args, **kwargs):
        url = self.get_argument('qr-url')  # type:str
        print(url)
        if url is not None:
            pj = Pingjiao(url, dry_run=False)
            pj.run()
        self.write('work on')


class WatchLogHandler(BaseHandler):
    def get(self):
        log_file = set(os.listdir('log'))-{'tornado.log'}
        log_html=''
        for file in log_file:
            log_html+='<h1>{}</h1>'.format(file)
            with open('log/'+file,'r',encoding='utf-8') as f:
                raw = f.read()
                raw = raw.replace('\n','<br>')
                log_html+='<p class="lead">{}</p>'.format(raw)
        self.render('watch_log.html',logs=log_html)


class TmpHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('tmp.html')


if __name__ == '__main__':
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bobo=",
        "xsrf_cookies": False,
        "login_url": "/login",
        'debug': True,
        'autoreload': True
    }

    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/index", IndexHandler),
            (r"/dict", DictHandler),
            (r'/qrcode', QRCodeHandler),
            (r'/tmp', TmpHanlder),
            (r'/log', WatchLogHandler)
        ],
        **settings
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
