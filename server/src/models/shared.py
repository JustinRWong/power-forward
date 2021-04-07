# apps.shared.models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy_session import flask_scoped_session
import pymongo

import uuid
import os
from datetime import datetime

MONGO_DB_CONNECTION_STRING = os.environ.get('MONGO_DB_CONNECTION_STRING')
mongo_client = pymongo.MongoClient(MONGO_DB_CONNECTION_STRING)
web_db = mongo_client.web
web_suggestions = web_db.suggestions
web_visitors = web_db.visitors
# DB_CONNECTION_STRING = os.environ.get('DATABASE_URL')
# # print(DB_CONNECTION_STRING)
# engine = create_engine(DB_CONNECTION_STRING)
# session_factory = sessionmaker(bind=engine)
#
# db = SQLAlchemy()
