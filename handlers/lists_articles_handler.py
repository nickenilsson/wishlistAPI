from tornado import web
from pymongo import MongoClient
import mongodb_helper
from bson.objectid import ObjectId
from base_handler import BaseHandler

class ListsArticlesHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(ListsArticlesHandler, self).__init__(*args, **kwargs)
		self.collection_articles = MongoClient().wishlist.articles


	def get(self, user_id, list_id):

		articles = self.list_helper.get_articles_in_list(list_id)
		response = {
			'articles': articles
		}

		self.write(response)
		self.finish()

	def post(self, user_id, list_id):
		title = self.get_argument('title')
		description = self.get_argument('description', None)
		image_url = self.get_argument('imageUrl')

		article_doc = {
			'userID': user_id,
			'listID': list_id,
			'title': title,
			'description': description,
			'imageUrl': image_url
		}
		mongodb_helper.insert(article_doc, self.collection_articles)


		pass