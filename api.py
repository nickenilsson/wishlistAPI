import tornado
from tornado.options import define, options
from tornado import ioloop, web, httpserver

from handlers.user_handler import UserHandler


define("port", default=8080, help="run on the given port ", type=int)


class WishlistApi(web.Application):
	"""
		Defines the tornado services
	"""

	def __init__(self):
		web.Application.__init__(self,
								 [
									 (r"/(userID)/wishlists", UserHandler),
									 (r"/(userID)/wishlists/(wishlistID)"),
									 (r"/(userID)/articles/(articleID))")
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