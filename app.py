import os
import tornado
import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.template

def gen_url(word):
    return 'http://cn.bing.com/dict/search?q={}&go=%E6%90%9C%E7%B4%A2&qs=n&form=Z9LH5&sp=-1&pq={}&sc=8-5&sk=&cvid=1026B339A8EA48DEA3EC59C4B2CFCD14'.format(
        word, word)


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
        self.render('LT_boostrap.html')


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

        ],
        **settings
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()