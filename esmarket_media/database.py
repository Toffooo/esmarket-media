import json

import pymysql
import sqlalchemy
from sqlalchemy import TEXT, Column, Integer, TypeDecorator, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DATABASE_URL


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = Column(Integer, autoincrement=True, primary_key=True)


pymysql.install_as_MySQLdb()
engine: sqlalchemy.engine.base.Engine = create_engine(DATABASE_URL, pool_recycle=1800)
session_factory: sqlalchemy.orm.session.sessionmaker = sessionmaker(
    bind=engine, autocommit=True
)
session = scoped_session(session_factory)
base = declarative_base()


class JSONEncodedDict(TypeDecorator):  # noqa
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)


JsonType = MutableDict.as_mutable(JSONEncodedDict)
ListType = MutableList.as_mutable(JSONEncodedDict)
