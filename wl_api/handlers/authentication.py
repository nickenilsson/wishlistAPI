import json

import tornado
import requests

from base import BaseHandler
from wl_api.models import User


class AuthenticationHandler(BaseHandler):

    def post(self):

        cookie_user_fb = self.get_secure_cookie('user')
        user = None
        if cookie_user_fb:
            cookie_user_fb = tornado.escape.json_decode(cookie_user_fb)
            user = self.db_helper.get_user(cookie_user_fb['_id'])

        if not user:
            fb_access_token = self.get_argument('facebook_token')
            user = self.get_authenticated_fb_user(fb_access_token)

            existing_user = self.db_helper.get_user_by_fb_id(user['facebook_id'])
            if not existing_user:
                user_id = self.db_helper.save_user(user)
                user['_id'] = str(user_id)
            else:
                user = existing_user
            self.set_secure_cookie('user', tornado.escape.json_encode(user.store))

        self.write({'response': {'user': user.store}})
        self.finish()


    def get_authenticated_fb_user(self, fb_access_token):
        app_access_token = self.get_app_access_token()
        template_url = 'https://graph.facebook.com/debug_token?input_token={0}&access_token={1}'
        url = template_url.format(fb_access_token, app_access_token)
        response = json.loads(requests.get(url).text)
        if not response['data'].get('is_valid') is True:
            raise tornado.web.HTTPError(403, 'User access token is not valid')

        user = self.get_user_info(response['data']['user_id'], fb_access_token)
        return user


    def get_user_info(self, user_id, user_access_token):
        template_url = 'https://graph.facebook.com/{0}?access_token={1}&fields=email,name,picture'
        url = template_url.format(user_id, user_access_token)
        user_info = json.loads(requests.get(url).text)
        user = User(name=user_info['name'], email=user_info['email'], facebook_id=user_info['id'])
        return user

    def get_app_access_token(self):
        template_url = 'https://graph.facebook.com/oauth/access_token?%20client_id={0}&client_secret={1}&grant_type=client_credentials'
        url = template_url.format(self.settings['FACEBOOK_APP_ID'], self.settings['FACEBOOK_APP_SECRET'])
        response = requests.get(url)
        app_access_token = response.text.replace('access_token=', '')
        return app_access_token




