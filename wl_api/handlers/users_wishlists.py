import tornado
import tornado.web
from bson.objectid import ObjectId

from wl_api.handlers.base import BaseHandler
from wl_api.models import WishList


class UsersWishlistsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        if user_id.lower() == 'me':
            user = self.get_current_user()
            user_id = user['_id']
        else:
            if not ObjectId.is_valid(user_id):
                raise tornado.web.HTTPError(400, 'Invalid ObjectId')

        page = self.get_argument('page', 1)
        if page < 1:
            raise tornado.HTTPError('Page number must be larger than zero')
        size = self.get_argument('size', 200)
        start = page - 1 * size

        wlists = self.db_helper.get_users_wishlists(user_id, start, size)

        self.write({'response': wlists})
        self.finish()


    @tornado.web.authenticated
    def post(self, user_id):
        if not user_id == 'me':
            raise tornado.web.HTTPError(500, "User can only post lists to his/her own account. Like: /users/me/wishlists")
        user = self.get_current_user()
        wlist = self.get_wishlist_from_args()
        wlist['_author_id'] = user['_id']
        self.db_helper.create_wishlist(user_id=ObjectId(user['_id']), wishlist=wlist)
        self.respond_ok()





