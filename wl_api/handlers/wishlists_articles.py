

import tornado

from wl_api.handlers.base import BaseHandler


class WishlistArticlesHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, wishlist_id):

        page = self.get_argument('start', 1)
        if page < 1:
            raise tornado.HTTPError('Page cannot be less that 1')
        size = self.get_argument('size', 200)
        start = (page - 1) * size

        wishlist = self.db_helper.get_wishlist(wishlist_id)

        self.write({'response': wishlist.store})



    @tornado.web.authenticated
    def post(self):
        pass