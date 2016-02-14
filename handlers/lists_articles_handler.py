from base_handler import BaseHandler

class ListsArticlesHandler(BaseHandler):

	def __init__(self, *args, **kwargs):
		super(ListsArticlesHandler, self).__init__(*args, **kwargs)


	def get(self, user_id, list_id):
		articles = self.list_helper.get_articles_in_list(list_id)
		response = {
			'articles': articles
		}

		self.write(response)
		self.finish()

	def post(self, user_id, list_id):
		title = self.get_argument('title')
		description = self.get_argument('description', None)
		image_url = self.get_argument('imageUrl')

		self.list_helper.insert_article(user_id, list_id, title=title, description=description, image_url=image_url)
		self.finish()

		pass