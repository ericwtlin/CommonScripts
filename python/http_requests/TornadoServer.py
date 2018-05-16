
"""
Simple HTTP server by tornado
Validated on Python3.6
"""

import ujson as json
import tornado.web
import tornado.httpserver
from tornado.options import define, options

define("port", default=8889, type=int)


class DealHandler(tornado.web.RequestHandler):
    def get(self):
        website = self.get_argument("website", None)
        city = self.get_argument("city", None)
        year = self.get_argument("year", None)
        month = self.get_argument("month", None)

        info = {
            'website': website,
            'city': city,
            'year': year,
            'month': month
        }
        self.write(json.dumps(info))


class ExampleHandler(tornado.web.RequestHandler):
    def get(self):
        who = self.get_argument("who", None)
        if who:
            self.write("GET: Hello, " + who)
        else:
            self.write("GET: Hello World!")

    def post(self):
        who = self.get_argument("who", None)
        if who:
            self.write("POST: Hello, " + who)
        else:
            self.write("POST: Hello World!")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", ExampleHandler),
            (r"/deal", DealHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, settings)


def create_server():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    create_server()