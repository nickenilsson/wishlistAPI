import tornado

from wl_api.handlers.base import BaseHandler


class UsersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):

        page = self.get_argument('start', 1)
        if page < 1:
            raise tornado.HTTPError('Page cannot be less that 1')
        size = self.get_argument('size', 200)
        start = (page - 1) * size

        if user_id == 'me':
            user = self.get_current_user()
        else:
            user = None
        wishlists = self.db_helper.get_users_wishlists(user['_id'], start, size)
        user['wishlists'] = wishlists
        self.write({'response': {'user': user.store}})

    @tornado.web.authenticated
    def post(self):
        pass