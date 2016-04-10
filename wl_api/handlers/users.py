import tornado

from wl_api.handlers.base import BaseHandler


class UsersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):

        start = self.get_argument('start', 0)
        size = self.get_argument('size', 10)
        if user_id == 'me':
            user = self.get_current_user()
        else:
            user = None
        wishlists = self.db_helper.get_users_wishlists(user['_id'], start, size)
        print "wishlists: ", wishlists
        user['wishlists'] = wishlists
        self.write({'response': {'user': user.store}})

    @tornado.web.authenticated
    def post(self):
        pass