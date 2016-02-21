from tornado import web
import db_helper

class BaseHandler(web.RequestHandler):


	def __init__(self, *args, **kwargs):
		super(BaseHandler, self).__init__(*args, **kwargs)
		self.db_helper = db_helper.DBHelper('mongo.aws')

	def display_error(self, status_code, message):
		self.set_status(status_code)
		self.write({
			'Status': status_code,
			'Message': message
		})
		self.finish()