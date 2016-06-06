
from wl_api.handlers.base import BaseHandler
import tornado
from bson import ObjectId
from tornado import web


from settings import ARTICLE_STATE_RESERVED, ARTICLE_STATE_AVALIABLE, ARTICLE_STATE_PURCHASED


class ArticlesStatesHandler(BaseHandler):

    def put(self, article_id):
        state = self.get_argument('state').upper()
        user = self.get_current_user()

        if not state in (ARTICLE_STATE_AVALIABLE, ARTICLE_STATE_PURCHASED, ARTICLE_STATE_RESERVED):
            raise web.HTTPError(400, 'Article state: {0} not recognized. Available states are {1}'.format(
                state,
                (ARTICLE_STATE_PURCHASED, ARTICLE_STATE_AVALIABLE, ARTICLE_STATE_RESERVED)
            ))
        if not ObjectId.is_valid(article_id):
            raise tornado.web.HTTPError(400, 'Invalid ObjectId : {0}'.format(article_id))

        self.db_helper.update_article_state(state, article_id, user['_id'])
        self.respond_ok()

