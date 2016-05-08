from celery import Celery
celery_app = Celery('tasks', backend='redis://localhost', broker='amqp://')

@celery_app.task
def delete_wishlist_from_user(mongo_client, wishlist_id, user_id):
    mongo_client.users.update_one({'_id': user_id}, {'$pull': wishlist_id})
