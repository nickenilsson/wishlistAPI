from tornado import web
from pymongo import MongoClient
import time
import validators

class UserListHandler(web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(UserListHandler, self).__init__(*args, **kwargs)
		self.mongo_client = MongoClient()


	def write_error(self, status_code, **kwargs):
		self.set_status(**kwargs)
		self.finish()


	def get(self):
		user_id = str(self.get_argument('userID'))

		items = list(self.mongo_client.wishlist.user.find({'userID': user_id}))

		for i in items:
			i['_id'] = str(i['_id'])

		response = {
			'wishlist': items
		}

		self.write(response)
		self.finish()


	def post(self):

		image_url = self.get_argument('imageUrl', None)
		if image_url:
			try:
				validators.url(image_url)
			except validators.ValidationFailure, e:
				self.write_error({'status_code': 400, 'message': 'Invalid url'})

		wishlist_item = {
			'userID': self.get_argument('userID'),
			'title': self.get_argument('title'),
			'imageUrl': self.get_argument('imageUrl'),
			'createdAt': time.time()
		}
		self.mongo_client.wishlist.user.insert(wishlist_item)

