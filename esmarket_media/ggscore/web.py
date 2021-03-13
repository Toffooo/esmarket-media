import json
import typing as tp
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup as bs

from esmarket_media.ggscore.utils import WebPlayer


class ESMarket(ABC):
    """
    Web interface for ggscore site
    """

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def serialize(self):
        pass


class Site:
    def __init__(self, url: str, headers: tp.Optional[dict] = None) -> None:
        self.url = url
        self.headers = headers
        if self.headers is None:
            self.headers = {
                "accept": "*/*",
                "user-agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
                ),
            }

    def get_html(self, url: tp.Optional[str] = None) -> tp.Union[bytes, tp.NoReturn]:
        """
        Get HTML of web page

        :param url: URL of site
        :return: HTML content from web page
        """
        if url is None:
            url = self.url

        with requests.Session() as session:
            resp = session.get(url=url, headers=self.headers)

            if resp.status_code == 200:
                return resp.content

            else:
                raise RuntimeError("Site error")

    def get_html_by_pages(
        self, url: tp.Optional[str] = None
    ) -> tp.Generator[dict, dict, None]:
        """
        Scrape site pages by iterating over it

        :param url: Base URL of site | https://example.com/?page={page} - Follow this format
        :return: Generator with pages link and html
        """
        if url is None:
            url = self.url

        with requests.Session() as session:
            for page in range(1, 1000000):
                resp = session.get(url=url.format(page=page), headers=self.headers)
                if resp.status_code == 200:
                    yield {"html": resp.content, "link": resp.url}
                else:
                    yield None

    def get_soup(self, html: bytes):
        soup = bs(html, "lxml")
        return soup


class ESMarketPlayers(ESMarket):
    """
    ESMarketPlayers is interface to working with
    players from GGSCORE web service.
    """

    def __init__(self):
        self._players = WebPlayer(site=Site)
        self._get_players = None

    @property
    def scraped(self):
        return self._get_players

    def get(self, pages: int):
        self._get_players = self._players.get_players(pages_count=pages)
        return self

    def serialize(self):
        return (
            json.dumps(self._get_players)
            if self._get_players is not None
            else json.dumps({})
        )

    def __str__(self):
        return self.serialize()
