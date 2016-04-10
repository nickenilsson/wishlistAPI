import tornado
import tornado.web
from bson.objectid import ObjectId

from base import BaseHandler
from wl_api.models import WishList


class UsersWishlistsHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super(UsersWishlistsHandler, self).__init__(*args, **kwargs)

    @tornado.web.authenticated
    def get(self, user_id):
        if user_id.lower() == 'me':
            user = self.get_current_user()
            user_id = user['_id']

        start = self.get_argument('start', 0)
        size = self.get_argument('size', 10)

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
        wlist = WishList(name=name, description=description, image_url=image_url)
        self.db_helper.create_wishlist(user_id=ObjectId(user['_id']), wishlist=wlist)
        self.finish()


