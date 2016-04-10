import tornado
import tornado.web
from bson.objectid import ObjectId

from base import BaseHandler
from wl_api.models import WishList


class UsersWishlistsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        if user_id.lower() == 'me':
            user = self.get_current_user()
            user_id = user['_id']

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
        name = self.get_argument('name')
        description = self.get_argument('description', '')
        image_url = self.get_argument('imageUrl', '')
        wlist = WishList(name=name, description=description, image_url=image_url, author=user['_id'])
        self.db_helper.create_wishlist(user_id=ObjectId(user['_id']), wishlist=wlist)
        self.finish()


