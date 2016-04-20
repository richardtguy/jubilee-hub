# this module includes configuration information for the app

# set up paths to SQL database and migration repository
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# configuration settings for flask development server
DEBUG = False
HOST = "0.0.0.0"
PORT = "5000"

# Secret key for API
KEY = '6ABC61D3E5C546AEF558AF34E1E92'