from pymongo import MongoClient

from bson.objectid import ObjectId

from wl_api.models import User, WishList
import tornado.web



class DBHelper(object):

    def __init__(self, host='localhost'):
        self.mongo_client = MongoClient(host).wishlist


    def _fix_doc_before_insert(self, doc):
        if isinstance(doc, dict):
            for k, v in doc.items():
                if k.startswith('_'):
                    doc[k] = ObjectId(v) if not isinstance(v, ObjectId) else v
                else:
                    self._fix_doc_before_insert(v)
        elif isinstance(doc, list):
            for i in doc:
                self._fix_doc_before_insert(i)
        return doc

    def _fix_doc_after_read(self, doc):
        if isinstance(doc, dict):
            for k, v in doc.items():
                if isinstance(v, ObjectId):
                    doc[k] = str(v)
                else:
                    self._fix_doc_after_read(v)
        elif isinstance(doc, list):
            for i in xrange(0, len(doc)):
                if isinstance(doc[i], ObjectId):
                    doc[i] = str(doc[i])
                else:
                    self._fix_doc_after_read(doc[i])
        return doc


    def set_image_for_wishlist(self, wish_list):
        if wish_list['articles']:
            wish_list['image_url'] = wish_list['articles'][0].get('image_url', '')
        return wish_list


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
        wishlists = map(self.set_image_for_wishlist, map(self._fix_doc_after_read, self.mongo_client.wishlists.find({'_id': {'$in': list_ids}})))
        return wishlists

    def create_wishlist(self, user_id, wishlist):
        wishlist['articles'] = [] if not wishlist.get('articles') else wishlist['articles']
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        wishlist_id = self.mongo_client.wishlists.insert(self._fix_doc_before_insert(wishlist.store))
        self.mongo_client.users.update({'_id': ObjectId(user_id)}, {'$push': {'wishlists': wishlist_id}})


    def get_wishlist(self, wish_list_id):
        wish_list_id = ObjectId(wish_list_id) if not isinstance(wish_list_id, ObjectId) else wish_list_id
        doc = self.mongo_client.wishlists.find_one({'_id': wish_list_id})
        wish_list = WishList(**self._fix_doc_after_read(doc))
        if wish_list['articles']:
            wish_list['image_url'] = wish_list['articles'][0].get('image_url')
        self.set_image_for_wishlist(wish_list)
        return wish_list


    def add_article_to_list(self, article, user_id, wish_list_id):
        wish_list_id = ObjectId(wish_list_id) if not isinstance(wish_list_id, ObjectId) else wish_list_id
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        article = self._fix_doc_before_insert(article.store)
        article['_id'] = ObjectId()

        query = {'_id': wish_list_id, '_author_id':user_id}

        result = self.mongo_client.wishlists.update_one(query, {'$push': {'articles': article}})
        return result

    #TODO: Make sure that only the author can edit articles
    def update_article(self, article):
        article = self._fix_doc_before_insert(article.store)
        return self.mongo_client.wishlists.update_one( {'articles._id':article['_id']},
                                                {'$set':{'articles.$.{0}'.format(k):v for k, v in article.items()}})

    def update_wishlist(self, wishlist_id, wishlist):
        wishlist_id = ObjectId(wishlist_id) if not isinstance(wishlist_id, ObjectId) else wishlist_id
        wishlist.pop('articles')
        wishlist = self._fix_doc_before_insert(wishlist)
        return self.mongo_client.wishlists.update_one({'_id': wishlist_id}, {'$set':{k:v for k,v in wishlist.items()}})

    def delete_article(self, article_id):
        article_id = ObjectId(article_id) if not isinstance(article_id, ObjectId) else article_id
        return self.mongo_client.wishlists.update_one({'articles._id': article_id}, {'$pull': {'_id': article_id}})


    def delete_wishlist(self, wish_list_id, user_id):
        wish_list_id = ObjectId(wish_list_id) if not isinstance(wish_list_id, ObjectId) else wish_list_id
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        self.mongo_client.wishlists.remove({'_id': wish_list_id, '_author_id': user_id})
        pass


    def delete_wishlist_from_all_users(self, wishlist_id):

        pass
