
from bson.objectid import ObjectId

def stringcast_ids(docs):
	for d in docs:
		d['_id'] = str(d['_id'])

def objectid_cast_ids(docs):
	for d in docs:
		d['_id'] = ObjectId(d['_id'])