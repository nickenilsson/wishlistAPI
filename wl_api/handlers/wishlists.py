import tornado
import tornado.web
from bson.objectid import ObjectId

from wl_api.handlers.base import BaseHandler
from wl_api.models import WishList


class WishlistsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, wishlist_id):
        self.write({'response': self.db_helper.get_wishlist()})
        self.finish()


    @tornado.web.authenticated
    def put(self, wishlist_id, wishlist):
        wishlist = self.get_wishlist_from_args()
        self.db_helper.update_wishlist(wishlist_id, wishlist)
        self.respond_ok()


    @tornado.web.authenticated
    def delete(self, wishlist_id):
        user = self.get_current_user()
        self.db_helper.delete_wishlist(wishlist_id, user['_id'])


