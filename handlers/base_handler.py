from tornado import web
import mongodb_helper

class BaseHandler(web.RequestHandler):


	def __init__(self, *args, **kwargs):
		super(BaseHandler, self).__init__(*args, **kwargs)
		self.list_helper = mongodb_helper.ListHelper('54.84.3.211')

	def display_error(self, status_code, message):
		self.set_status(status_code)
		self.write({
			'Status': status_code,
			'Message': message
		})
		self.finish()