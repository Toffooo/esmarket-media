from sqlalchemy import Column, Integer, String

from esmarket_media.database import base, session
from esmarket_media.exceptions import TooManyArgumentsProvided

local_session = session()


class ModelMixin:
    @classmethod
    def all(cls):
        return local_session.query(cls).all()

    @classmethod
    def get(cls, **kwargs):
        if len(kwargs.keys()) > 1:
            raise TooManyArgumentsProvided(
                "Too many arguments provided to `get` method."
            )

        data = (
            local_session.query(cls)
            .filter(*[getattr(cls, key) == value for key, value in kwargs.items()])
            .limit(1)
            .one()
        )
        return data

    @classmethod
    def filter(cls, **kwargs):
        data = (
            local_session.query(cls)
            .filter(*[getattr(cls, key) == value for key, value in kwargs.items()])
            .limit(1)
            .one()
        )
        return data

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)  # noqa
        local_session.add(instance)
        local_session.commit()
        return instance

    def save(self):
        local_session.add(self)
        local_session.commit()
        return self

    def delete(self):
        local_session.delete(self)
        local_session.commit()
        return self

    def __repr__(self):
        columns = list(self.__table__.columns)  # noqa
        return "<{model_name}({expression})>".format(
            model_name=self.__class__.__name__.capitalize(),  # noqa
            expression=", ".join(
                [f"{column.name}={getattr(self, column.name)}" for column in columns]
            ),
        )


class Player(base, ModelMixin):
    name = Column(String(length=225))
    twitch_followers_count = Column(Integer, default=0)
    instagram_followers_count = Column(Integer, default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
