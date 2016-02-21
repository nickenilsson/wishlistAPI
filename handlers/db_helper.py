
from bson.objectid import ObjectId
from pymongo import MongoClient

class DBHelper(object):

	def __init__(self, host):
		self.mongo_client = MongoClient(host).wishlist


	def stringcast_ids(self, docs):
		def s_cast_doc(doc):
			for k,v in doc.items():
				if k == '_id' or k.endswith('ID'):
					doc[k] = str(v)
		if isinstance(docs, list):
			[s_cast_doc(d) for d in docs]
		elif isinstance(docs, dict):
			s_cast_doc(docs)
		return docs


	def objectid_cast_ids(self, docs):
		def oid_cast_doc(doc):
			for k,v in doc.items():
				if k == '_id' or k.endswith('ID'):
					doc[k] = ObjectId(v)

		if isinstance(docs, list):
			[oid_cast_doc(d) for d in docs]
		elif isinstance(docs, dict):
			oid_cast_doc(docs)
		return docs


	def create_user(self, user_id, username):
		pass


	def get_user(self, user_id):
		query = self.objectid_cast_ids({'_id': user_id})
		return self.stringcast_ids(self.mongo_client.users.find_one(query))


	def get_users_lists(self, user_id, start=0, size=10):
		query = self.objectid_cast_ids({'userID': user_id})
		return [self.stringcast_ids(d) for d in self.mongo_client.lists.find(query)]


	def create_list(self, user_id, title, description=None, image_url=None):
		doc = {
			'userID': user_id,
			'title': title,
			'description': description,
			'imageUrl': image_url
		}
		self.objectid_cast_ids(doc)
		return self.mongo_client.lists.insert(doc)


	def save_list(self, user_id, list_id):
		r_query = self.objectid_cast_ids({'_id': user_id})
		w_query = self.objectid_cast_ids({'$push': {'lists': list_id}})
		self.mongo_client.update(r_query, w_query)


	def get_list_contents(self, list_id, size=10):
		query = self.objectid_cast_ids({'listID': list_id})
		return [self.stringcast_ids(d) for d in self.mongo_client.articles.find(query, limit=size)]


	def insert_article(self, user_id, list_id, title, description=None, image_url=None):
		article = self.objectid_cast_ids({
			'userID': user_id,
			'listID': list_id,
			'title': title,
			'description': description,
			'imageUrl': image_url
		})
		return self.mongo_client.articles.insert(article)


	def get_article_contents(self, article_id):
		query = self.objectid_cast_ids({'_id': article_id})
		return [self.stringcast_ids(d) for d in self.mongo_client.find(query)]
