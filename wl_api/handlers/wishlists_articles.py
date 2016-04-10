

import tornado

from wl_api.handlers.base import BaseHandler
from wl_api.models import Article


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
        user = self.get_current_user()
        name = self.get_argument('name')
        description = self.get_argument('description', None)
        image_url = self.get_argument('imageUrl', None)
        article = Article(name=name, description=description, image_url=image_url)
        self.db_helper.add_article_to_list(article, user['_id'], wishlist_id)
        self.finish()