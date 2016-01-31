from tornado import web
from pymongo import MongoClient

class UserListHandler(web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(UserListHandler, self).__init__(*args, **kwargs)
		self.mongo_client = MongoClient()

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

		wishlist_item = {
			'userID': self.get_argument('userID'),
			'title': self.get_argument('title'),
			'imageUrl': self.get_argument('imageUrl')
		}
		self.mongo_client.wishlist.user.insert(wishlist_item)