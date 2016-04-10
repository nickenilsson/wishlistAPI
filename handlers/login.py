from base import BaseHandler
import tornado.web
import tornado.auth


class FacebookGraphLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):

        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri='http://192.168.51.121:8080/login',
                client_id=self.settings["FACEBOOK_APP_ID"],
                client_secret=self.settings["FACEBOOK_APP_SECRET"],
                code=self.get_argument("code"),
                callback=self._on_login
            )
            return
        self.authorize_redirect(redirect_uri='http://192.168.51.121:8080/login',
                                client_id=self.settings["FACEBOOK_APP_ID"],
                                extra_params={"scope": "email"}
        )


    def _on_login(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie('fb_user', tornado.escape.json_encode(user))

        if not self.mongo_db.users.find_one({'facebookData.id': user['id']}):
            self.mongo_db.users.insert({
                'facebookData': user,
                'name': user['name'],
                'lists': []
            })

        #self.write("Logged in: ", user)
        self.finish()


