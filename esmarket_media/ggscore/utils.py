import re
from typing import List, Optional

from esmarket_media.ggscore.resources import urls
from esmarket_media.models import Player
from settings import GGSCORE_BASE_LINK


def union_lists(value: list):
    return_list = []

    for element in value:
        if isinstance(value, list):
            return_list.extend(element)
        else:
            return_list.extend(element)

    return return_list


class WebPlayer:
    def __init__(self, site) -> None:
        self.site = site(url=urls.GGSCORE_PLAYERS_URL)

    @staticmethod
    def process_alternative_names(alternative_names_text: str) -> list:
        """
        Process alternative names

        :param alternative_names_text: Scraped text about alternative names
        :return: Alternative names list
        """
        names = alternative_names_text.replace("This user has also played as:", "")
        if "/" in names:
            names = names.split("/")[0].strip()
            names = [name.strip() for name in names.split(",")]

        return [names.strip()] if isinstance(names, str) else names

    def handle_profile_page_html(self, link: str, player: dict) -> dict:
        """
        Parse main info about player from player's page

        :param link: Link to player's page
        :param player: Player dict
        :return: Player data
        """
        html = self.site.get_html(url=link)
        soup = self.site.get_soup(html)

        names = " ".join(soup.find("div", attrs={"class": "well"}).text.strip().split())
        alternative_names = self.process_alternative_names(alternative_names_text=names)
        player_data: dict = {
            **player,
            "alternative_names": alternative_names,
            "teams_history": [],
        }

        team_history = (
            soup.find("table", attrs={"class": "teamWins"}).find("tbody").find_all("tr")
        )

        for team in team_history:
            team_name = team.find_all("td")[1].find("a").text.strip()
            matches = team.find_all("td")[2].text.strip()

            start_date = (
                team.find_all("td")[3]
                .find("span", attrs={"class": "sct"})
                .get("data-time")
            )
            end_date = (
                team.find_all("td")[3]
                .find("span", attrs={"class": "sct"})
                .get("data-compare")
            )

            player_data["teams_history"].append(
                {
                    "team_name": team_name,
                    "matches": matches,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )

        return player_data

    def handle_main_page_html(self, soup) -> Optional[List[dict]]:
        """
        Process players from HTML

        :param soup: Beautiful soup type object
        :return: List of Player type model objects
        """
        players = []
        mtable = soup.find("table", attrs={"class": "mtable"})

        if mtable is None:
            return None

        items = mtable.find_all("tr", attrs={"class": "t-item"})

        for item in items:
            earned = re.findall(
                r"^\$\s(\d+)", item.find("td", attrs={"class": "scm"}).text.strip()
            )

            player_dict = {
                "ggscore_name": "".join(item.find("td").find("a").text.strip().split()),
                "earned": int(earned[0]) if len(earned) > 0 else 0,
                "form": item.find_all("td")[3].text.strip(),
                "rating": item.find_all("td")[4].text.strip(),
            }

            team_history = self.handle_profile_page_html(
                link=GGSCORE_BASE_LINK + item.find("td").find("a").get("href"),
                player=player_dict,
            )

            players.append(team_history)

        return players

    def get_players(self, pages_count: int) -> List[Player]:
        """
        Get players from web page

        :param pages_count: How much pages need to scrape from site | Limit = 1000000
        :return: List of Player type model objects
        """
        pages = self.site.get_html_by_pages()
        all_players: List[Player] = []

        for index, page in enumerate(pages):
            if index == pages_count:
                return all_players

            soup = self.site.get_soup(html=page["html"])
            players = self.handle_main_page_html(soup=soup)
            if players is None:
                return all_players

            all_players += players
