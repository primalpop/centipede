from flask import Flask
from app.config import BaseConfig
from app.lib.LocationSearch import LocationSearch
import logging
from logging.handlers import RotatingFileHandler


def app_bootstrap():

	app.locationsearch = LocationSearch(db_host=app.config['LOCATION_DB_SERVER'], 
									db=app.config['LOCATION_DB'], 
									db_collection=app.config['LOCATION_DB_COLLECTION'])


	app.logger.debug("Bootstrap completed")

app = Flask(__name__)
app.config.from_object(BaseConfig)


file_handler = RotatingFileHandler(app.config['SERVER_LOGFILE'], 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(module)s.%(funcName)s: %(message)s'))
app.logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)	
app.logger.debug('Initializing log')

#app.before_first_request(app_bootstrap)

from app import views
