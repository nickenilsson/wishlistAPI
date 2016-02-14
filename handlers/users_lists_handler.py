from base_handler import BaseHandler

class UsersListsHandler(BaseHandler):

	def __init__(self, *args, **kwargs):
		super(UsersListsHandler, self).__init__(*args, **kwargs)


	def get(self, user_id):
		size = self.get_argument('size', 10)

		lists = self.list_helper.get_lists(user_id, size=size)
		response = {
			'lists': lists
		}
		self.write(response)
		self.finish()


	def post(self, user_id):
		title = self.get_argument('title')
		description = self.get_argument('description', None)
		image_url = self.get_argument('imageUrl', None)

		self.list_helper.insert_list(user_id=user_id, title=title, description=description, image_url=image_url)

		self.finish()

