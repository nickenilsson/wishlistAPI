from base_handler import BaseHandler

class UsersListsHandler(BaseHandler):

	def __init__(self, *args, **kwargs):
		super(UsersListsHandler, self).__init__(*args, **kwargs)


	def get(self, user_id):
		start = self.get_argument('start', 0)
		size = self.get_argument('size', 10)

		lists = self.db_helper.get_users_lists(user_id, start=start, size=size)
		print lists
		response = {
			'lists': lists
		}
		self.write(response)
		self.finish()


	def post(self, user_id):
		title = self.get_argument('title')
		description = self.get_argument('description', '')
		image_url = self.get_argument('imageUrl', '')

		self.db_helper.create_list(user_id=user_id, title=title, description=description, image_url=image_url)

		self.finish()

