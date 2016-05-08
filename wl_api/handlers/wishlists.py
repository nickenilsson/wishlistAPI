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



    def put(self, wishlist_id, wishlist):
        wishlist = self.get_wishlist_from_args()
        self.db_helper.update_wishlist(wishlist_id, wishlist)
        self.respond_ok()


    @tornado.web.authenticated
    def delete(self, wishlist):
        user = self.get_current_user()


