import tornado
from tornado.options import define, options
from tornado import ioloop, web, httpserver

from handlers.user_lists import UserListHandler


define("port", default=8041, help="run on the given port ", type=int)

class WishlistApi(web.Application):
    """
        Defines the tornado services
    """
    def __init__(self):
        web.Application.__init__(self,
                                 [
                                     (r"/wishlist", UserListHandler)
                                 ],
                                 autoreload=True)

def start(port):
    application = WishlistApi()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    start(options.port)