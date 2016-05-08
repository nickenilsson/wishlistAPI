from wl_api.handlers.base import BaseHandler
import tornado
from bson import ObjectId

class ArticlesHandler(BaseHandler):

    @tornado.web.authenticated
    def put(self, article_id):
        if not ObjectId.is_valid(article_id):
            raise tornado.web.HTTPError(400, 'Invalid ObjectId : {0}'.format(article_id))
        article = self.get_article_from_args()
        article['_id'] = article_id
        self.db_helper.update_article(article)
        self.respond_ok()


    @tornado.web.authenticated
    def delete(self, article_id):
        if not ObjectId.is_valid(article_id):
            raise tornado.web.HTTPError(400, 'Invalid ObjectId : {0}'.format(article_id))
        self.db_helper.delete_article(article_id)
        self.respond_ok()
