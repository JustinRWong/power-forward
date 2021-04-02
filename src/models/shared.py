# apps.shared.models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import postgresql; postgresql.UUID()
from flask_sqlalchemy_session import flask_scoped_session
import uuid
import os
from vars import *

print('CONNECTION STRING')
print(DB_CONNECTION_STRING)
# engine = create_engine(DB_CONNECTION_STRING)
# session_factory = sessionmaker(bind=engine)

db = SQLAlchemy()
