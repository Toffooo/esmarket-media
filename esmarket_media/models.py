from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin

from esmarket_media.database import JsonType, ListType, base, engine, session


class AbstractModel(base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        pass


class Player(AbstractModel):
    __tablename__ = "players"

    id = Column(Integer, autoincrement=True, primary_key=True)
    ggscore_name = Column(String(length=225))
    strength = Column(Integer, default=0)
    alternative_names = Column(ListType, default=[])
    form = Column(Integer, default=0)
    earned = Column(Integer, default=0)
    twitch_meta = Column(JsonType, default={})
    instagram_meta = Column(JsonType, default={})
    rating = Column(Integer, default=0)

    teams_history = relationship("TeamHistory", back_populates="player")


class TeamHistory(AbstractModel):
    __tablename__ = "team_histories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_name = Column(String(length=255))
    matches = Column(Integer, default=0)
    start_date = Column(Integer, default=0)
    end_date = Column(Integer, default=0)

    player = relationship("Player", back_populates="teams_history")


base.metadata.create_all(engine)
AbstractModel.set_session(session)
