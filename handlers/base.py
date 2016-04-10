from tornado import web
import db_helper
from pymongo import MongoClient
import tornado


class BaseHandler(web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.db_helper = db_helper.DBHelper('mongo.aws')
        self.mongo_db = MongoClient('mongo.aws').wishlist

    def get_current_user(self):
        cookie_user_fb = self.get_secure_cookie('user')
        if cookie_user_fb:
            cookie_user_fb = tornado.escape.json_decode(cookie_user_fb)
            user = self.db_helper.get_user(cookie_user_fb['_id'])
            return user


    def display_error(self, status_code, message):
        self.set_status(status_code)
        self.write({
            'Status': status_code,
            'Message': message
        })
        self.finish()