from tornado import web
from pymongo import MongoClient

class UserListHandler(web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(UserListHandler, self).__init__(*args, **kwargs)
		self.mongo_client = MongoClient()

	def get(self):
		user_id = str(self.get_argument('userID'))

		items = list(self.mongo_client.wishlist.user.find({'userID' : user_id}, {'_id' : 0}))

		response = {
			'wishlist' : items
		}

		self.write(response)
		self.finish()
