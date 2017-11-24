#!/usr/bin/env python
# coding: utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jerry.settings")
import django
if django.VERSION >= (1, 7):
    setup = django.setup()

from django.core.wsgi import get_wsgi_application

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.websocket

from tornado.options import options, define

from handlers import *
from ioloop import IOLoop


define('port', type=int, default=8559)


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    setting = {
        'cookie_secret': 'DFksdfsasdfkasdfFKwlwfsdfsa1204mx',
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'debug': False,
    }

    tornado_app = tornado.web.Application(
        [
            (r'/ws/terminal', WSHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__), "static"))),
            (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    options.parse_config_file('webssh.conf')
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address='0.0.0.0')
    IOLoop.instance().start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
