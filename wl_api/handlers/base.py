from tornado import web
from pymongo import MongoClient
import tornado
from wl_api.models import WishList, User, Article
from wl_api.handlers import db_helper


class BaseHandler(web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.db_helper = db_helper.DBHelper('mongo.aws')


    def get_current_user(self):
        cookie_user_fb = self.get_secure_cookie('user')
        if cookie_user_fb:
            cookie_user_fb = tornado.escape.json_decode(cookie_user_fb)
            user = self.db_helper.get_user(cookie_user_fb['_id'])
            return user

    def respond_ok(self):
        self.write({'response': 'Ok!'})
        self.finish()

    def display_error(self, status_code, message):
        self.set_status(status_code)
        self.write({
            'Status': status_code,
            'Message': message
        })
        self.finish()


    def get_user_from_args(self):

        pass


    def get_article_from_args(self):
        k_arguments = {}
        k_arguments['name'] = self.get_argument('name')
        k_arguments['description'] = self.get_argument('description', None)
        k_arguments['image_url'] = self.get_argument('imageUrl', None)
        k_arguments['state'] = self.get_argument('state', None)
        return Article(**k_arguments)



    def get_wishlist_from_args(self):
        k_arguments = {}
        k_arguments['name'] = self.get_argument('name')
        k_arguments['description'] = self.get_argument('description', '')
        k_arguments['image_url'] = self.get_argument('imageUrl', '')
        return WishList(**k_arguments)
