from pymongo import MongoClient

from bson.objectid import ObjectId

from wl_api.models import User


class DBHelper(object):

    def __init__(self, host='localhost'):
        self.mongo_client = MongoClient(host).wishlist


    def _fix_doc_before_insert(self, doc):
        if isinstance(doc, dict):
            for k, v in doc.items():
                if k.startswith('_'):
                    doc[k] = ObjectId(v) if not isinstance(v, ObjectId) else v
                self._fix_doc_before_insert(v)
        elif isinstance(doc, list):
            for i in doc:
                self._fix_doc_before_insert(i)
        return doc

    def _fix_doc_after_read(self, doc):

        if isinstance(doc, dict):
            for k, v in doc.items():
                if isinstance(v, ObjectId) or k.startswith('_'):
                    doc[k] = str(v)
                else:
                    self._fix_doc_after_read(v)
        elif isinstance(doc, list):
            for i in xrange(0, len(doc)):
                if isinstance(doc[i], ObjectId):
                    doc[i] = str(doc[i])
                else:
                    self._fix_doc_after_read(i)
        return doc



    def save_user(self, user):
        user['wishlists'] = [] if not user.get('wishlists') else user['wishlists']
        prepared_doc = self._fix_doc_before_insert(user.store)

        return self.mongo_client.users.insert(prepared_doc)


    def get_user(self, user_id):
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        result = self.mongo_client.users.find_one({'_id': user_id})
        if result:
            user_data = self._fix_doc_after_read(result)
            return User(**user_data)

    def get_user_by_fb_id(self, fb_id):
        result = self.mongo_client.users.find_one({'facebook_id': fb_id})
        if result:
            user_data = self._fix_doc_after_read(result)
            return User(**user_data)


    def get_users_wishlists(self, user_id, start=0, size=10):
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        list_ids = self.mongo_client.users.find_one({'_id': user_id}, {'wishlists': {'$slice': [start, size]}})['wishlists']

        wishlists = map(self._fix_doc_after_read, self.mongo_client.wishlists.find({'_id': {'$in': list_ids}}))

        return wishlists

    def create_wishlist(self, user_id, wishlist):
        wishlist['articles'] = [] if not wishlist.get('articles') else wishlist['articles']
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        wishlist_id = self.mongo_client.wishlists.insert(self._fix_doc_before_insert(wishlist.store))
        self.mongo_client.users.update({'_id': ObjectId(user_id)}, {'$push': {'wishlists': wishlist_id}})
