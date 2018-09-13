
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

class RawTextHandler(tornado.web.RequestHandler):

    def is_binary_content(self):
        content_type = self.request.headers.get("Content-Type", "text/plain")
        return (content_type == "application/binary")

    def post(self):
        if (not self.request.body):
            self.set_status(500)
            self.write("empty request")
            self.finish()
            return

        try:
            if self.is_binary_content():
                response = self.request.body
                self.set_header("Content-Type", "application/binary")
                self.write(response)
            else:
                response = self.request.body.decode('utf-8')
                req_split = self.request.body.decode('utf-8').split('\t')
                print(req_split)
                self.set_header("Content-Type", "text/plain")
                self.write(response)

            self.finish()
            return
        except Exception as e:
            self.set_status(500)
            self.write("internal server error: %s" % e)
            self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", ExampleHandler),
            (r"/deal", DealHandler),
            (r"/rawtext", RawTextHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, settings)


def create_server():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print('Server started...Listening on port %s' % str(options.port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    create_server()     # e.g. python TornadoServer.py --port=8080, or simply python TornadoServer.py