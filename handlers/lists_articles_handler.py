from base_handler import BaseHandler

class ListsArticlesHandler(BaseHandler):

	def __init__(self, *args, **kwargs):
		super(ListsArticlesHandler, self).__init__(*args, **kwargs)


	def get(self, list_id):
		articles = self.db_helper.get_list_contents(list_id)
		response = {
			'articles': articles
		}

		self.write(response)
		self.finish()


	def post(self, list_id):
		title = self.get_argument('title')
		description = self.get_argument('description', '')
		image_url = self.get_argument('imageUrl')

		self.db_helper.insert_article(list_id, title=title, description=description, image_url=image_url)
		self.finish()

		pass