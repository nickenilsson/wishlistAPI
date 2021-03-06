

import tornado

from wl_api.handlers.base import BaseHandler
from wl_api.models import Article
from bson import ObjectId


class WishlistArticlesHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, wishlist_id):

        page = self.get_argument('start', 1)
        if page < 1:
            raise tornado.HTTPError('Page cannot be less that 1')
        size = self.get_argument('size', 200)
        start = (page - 1) * size

        wishlist = self.db_helper.get_wishlist(wishlist_id)

        user = self.get_current_user()

        self.write({
            'response': {
                'wishlist': wishlist.store,
                'is_owner': wishlist['_author_id'] == user['_id']
            }
        })
        self.finish()


    @tornado.web.authenticated
    def post(self, wishlist_id):

        if not ObjectId.is_valid(wishlist_id):
            raise tornado.web.HTTPError(400, 'Invalid ObjectId')
        user = self.get_current_user()
        article = self.get_article_from_args()

        article_id = self.db_helper.add_article_to_list(article, user['_id'], wishlist_id)
        self.write({'response':{'message':'Article created successfully!', 'article_id': article_id}})