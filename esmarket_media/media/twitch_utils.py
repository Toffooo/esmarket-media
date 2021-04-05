import typing as tp

import twitch
from twitch.helix.resources.users import Users

from esmarket_media.models import Player
from settings import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

helix = twitch.Helix(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
_USER = tp.Union[tp.Union[int, str], tp.List[tp.Union[str, int]]]


class TwitchUserMixin:
    @staticmethod
    def get_users(users: tp.Union[_USER, tp.List[Player]]) -> Users:
        """
        Get user from media API by user's id or display_name

        :param users: List of display_names and ids or display_name or user's id
            || List of Player type model object
        :return: User instance
        """
        if all(True if isinstance(user, Player) else False for user in users):
            users = [user.ggscore_name for user in users]

        return helix.users(users)

    @staticmethod
    def get_followers_count(
        users: tp.Union[_USER, tp.List[Player]]
    ) -> tp.Dict[str, int]:
        """
        Get user's followers from media API by user's id or display_name

        :param users: List of display_names and ids or display_name or user's id
            || List of Player type model object
        :return: Dict with info about followers count
        """
        if all(True if isinstance(user, Player) else False for user in users):
            users = [user.ggscore_name for user in users]

        _users = TwitchUserMixin.get_users(users)
        return {user.display_name.lower(): user.followers().total for user in _users}
