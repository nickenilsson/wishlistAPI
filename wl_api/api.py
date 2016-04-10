import tornado
from tornado.options import define, options
from tornado import ioloop, web, httpserver

from handlers.users_wishlists import UsersWishlistsHandler
from handlers.users import UsersHandler
from handlers.login import FacebookGraphLoginHandler
from wl_api.handlers.authentication import AuthenticationHandler
from wl_api import settings


define("port", default=8080, help="run on the given port ", type=int)

class WishlistApi(web.Application):

    def __init__(self):
        web.Application.__init__(self,

                                 [
                                     (r"/users/authenticate/?", AuthenticationHandler),
                                     (r"/users/([A-Za-z0-9_]*)/?", UsersHandler),
                                     (r"/users/([A-Za-z0-9_]*)/wishlists/?", UsersWishlistsHandler),
                                     #(r"/lists/([A-Za-z0-9_]*)?", ListsHandler),
                                     #(r"/articles/([A-Za-z0-9_]*)?", ArticlesHandler)
                                 ],
                                 autoreload=True,
                                 **settings.settings


        )


def start(port):
    application = WishlistApi()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    start(options.port)