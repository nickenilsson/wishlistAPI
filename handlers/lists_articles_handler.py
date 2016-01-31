from tornado import web
from pymongo import MongoClient
import time
import validators
import mongo_id_helper

class ListsArticlesHandler(web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(ListsArticlesHandler, self).__init__(*args, **kwargs)
		self.collection_articles = MongoClient().wishlist.articles

	def get(self, user_id, list_id):
		articles = list(self.collection_articles.find({'listID': list_id}))
		mongo_id_helper.stringcast_ids(articles)
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
			'title': title,
			'description': description,
			'imageUrl': image_url
		}
		self.collection_articles.insert(article_doc)

		pass