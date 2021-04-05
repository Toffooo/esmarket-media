from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin

from .database import JsonType, ListType, base, engine, session


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

    @classmethod
    def update_or_create(cls, **kwargs):
        player = cls.where(ggscore_name=kwargs["ggscore_name"]).all()
        if len(player) == 0:
            player = cls.create(**kwargs)

        else:
            player[0].earned = kwargs["earned"]
            player[0].form = kwargs["form"]
            player[0].rating = kwargs["rating"]
            player[0].alternative_names = kwargs["alternative_names"]
            player = player[0].update()

        return player[0] if isinstance(player, list) and player else player


class TeamHistory(AbstractModel):
    __tablename__ = "team_histories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_name = Column(String(length=255))
    matches = Column(Integer, default=0)
    start_date = Column(Integer, default=0)
    end_date = Column(Integer, default=0)

    player = relationship("Player", back_populates="teams_history")

    @classmethod
    def update_or_create(cls, **kwargs):
        team = cls.where(
            team_name=kwargs["team_name"], player_id=kwargs["player_id"]
        ).all()
        if len(team) == 0:
            team = cls.create(**kwargs)
        else:
            team[0].matches = kwargs["matches"]
            team[0].start_date = kwargs["start_date"]
            team[0].end_date = kwargs["end_date"]
            team = team[0].update()

        return team


base.metadata.create_all(engine)
AbstractModel.set_session(session)
