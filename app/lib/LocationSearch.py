import logging
from logging import getLogger
from pymongo import MongoClient

class LocationSearch:
	client = None
	db = None
	collection = None

	SEARCH_PREFIX_MIN = 3

	def __init__(self, db_host, db, db_collection):
		self.logger = logging.getLogger("app.locationsearch")
		self.client = MongoClient(db_host)
		self.db = self.client[db]
		self.collection = self.db[db_collection]
		self.logger.debug("Successfully established mongo connection: {0}/{1}/{2}".format(db_host, db, db_collection))

	def search(self, prefix):
		if len(prefix) >= self.SEARCH_PREFIX_MIN:
			result_set = []
			#TODO: Edit the fields
			for result in self.collection.find( { "_id": { "$regex" : "^"+prefix, "$options": 'i' } }, limit=10):
				result_set.append(result)
			return result_set
		else:
			return []
