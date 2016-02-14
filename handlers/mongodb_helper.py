
from bson.objectid import ObjectId
from pymongo import MongoClient

class ListHelper(object):

	def __init__(self, host):
		self.mongo_client = MongoClient(host).wishlist
		self.COLLECTION_LISTS = "lists"
		self.COLLECTION_ARTICLES = "articles"


	def stringcast_ids(self, docs):
		def s_cast_doc(doc):
			for k,v in doc.items():
				if k == '_id' or k.endswith('ID'):
					k[k] = str(v)
		if isinstance(docs, list):
			[s_cast_doc(d) for d in docs]
		elif isinstance(docs, dict):
			s_cast_doc(docs)
		return docs


	def objectid_cast_ids(self, docs):
		def oid_cast_doc(doc):
			for k,v in doc.items():
				if k == '_id' or k.endswith('ID'):
					d[k] = ObjectId(v)

		if isinstance(docs, list):
			[oid_cast_doc(d) for d in docs]
		elif isinstance(docs, dict):
			oid_cast_doc(docs)
		return docs


	def get_lists(self, user_id, size=10):
		query = self.objectid_cast_ids({'userID': user_id})
		return [self.stringcast_ids(d) for d in self.mongo_client[self.COLLECTION_LISTS].find(query, limit=size)]


	def insert_list(self, user_id, title, description=None, image_url=None):
		doc = {
			'userID': user_id,
			'title': title,
			'description': description,
			'imageUrl': image_url
		}
		self.objectid_cast_ids(doc)
		return self.mongo_client[self.COLLECTION_LISTS].insert(doc)


	def get_articles_in_list(self, list_id, size=10):
		query = self.objectid_cast_ids({'listID': list_id})
		return [self.stringcast_ids(d) for d in self.mongo_client[self.COLLECTION_ARTICLES].find(query, limit=size)]


	def insert_article(self, user_id, list_id, title, description=None, image_url=None):
		article = self.objectid_cast_ids({
			'userID': user_id,
			'listID': list_id,
			'title': title,
			'description': description,
			'imageUrl': image_url
		})
		return self.mongo_client[self.COLLECTION_ARTICLES].insert(article)