import logging

from celery import Celery
from sqlalchemy.exc import OperationalError

from esmarket_media import ESMarketPlayers
from esmarket_media.media.twitch_utils import TwitchUserMixin
from esmarket_media.models import Player, TeamHistory
from settings import CeleryConfig

logger = logging.getLogger(__name__)
app = Celery("tasks")
app.config_from_object(CeleryConfig)

esplayers = ESMarketPlayers()


@app.task(name="playersupdate", autoretry_for=(OperationalError,))
def scrape_players_meta():
    esplayers.get(pages=1)  # script will stop by own

    for player in esplayers.scraped:
        logger.info("HANDLING PLAYER {player}".format(player=player["ggscore_name"]))

        _player = Player.update_or_create(
            ggscore_name=player["ggscore_name"],
            earned=player["earned"],
            form=int(player["form"].replace("%", "")),
            rating=int(player["rating"]),
            alternative_names=player["alternative_names"],
        )

        for team in player["teams_history"]:
            _ = TeamHistory.update_or_create(
                player_id=_player.id,
                team_name=team["team_name"],
                matches=team["matches"],
                start_date=team["start_date"],
                end_date=team["end_date"],
            )


@app.task(name="playersTwitchMetaUpdate", autoretry_for=(OperationalError,))
def scrape_players_twitch():
    players = Player.all()
    flc = TwitchUserMixin.get_followers_count(players)

    for player in players:
        logger.info(f"HANDLING PLAYER {player.ggscore_name}")
        meta = flc.get(player.ggscore_name.lower())
        if meta is None:
            continue

        player.twitch_meta = {"name": player.ggscore_name, "followers": meta}
        player.update()
