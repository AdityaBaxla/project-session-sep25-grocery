from flask_sqlalchemy import SQLAlchemy
from flask_security.core import Security
from flask_caching import Cache

db = SQLAlchemy()
security = Security()
cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_DEFAULT_TIMEOUT': 1})