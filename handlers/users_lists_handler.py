from tornado import web
from pymongo import MongoClient
import mongo_id_helper

class UsersListsHandler(web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(UsersListsHandler, self).__init__(*args, **kwargs)
		self.collection_lists = MongoClient().wishlist.lists

	def get(self, user_id):
		lists = list(self.collection_lists.find({'userID': user_id}))
		mongo_id_helper.stringcast_ids(lists)
		response = {
			'lists': lists
		}
		self.write(response)
		self.finish()

	def post(self, user_id):
		title = self.get_argument('title')
		list_doc = {
			'userID': user_id,
			'title': title
		}
		self.collection_lists.insert(list_doc)
		self.finish()

