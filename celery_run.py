import json
import logging.config

import click

from feed.tasks import scrape_players_meta, scrape_players_twitch

logger = logging.getLogger(__name__)


def setup_logging(filename: str = "./logging.json"):
    with open(filename) as f:
        config = json.load(f)
    logging.config.dictConfig(config)


def players():
    logger.info("Players is updating")
    scrape_players_meta.delay()


def twitch():
    logger.info("TWITCH META IS UPDATING")
    scrape_players_twitch.delay()


@click.command()
@click.option("--wtf", "-w")
def main(wtf):
    setup_logging()
    if wtf == "players":
        players()
    elif wtf == "twitch":
        twitch()


if __name__ == "__main__":
    main()
