import typing as tp

import twitch
from twitch.helix.resources.users import Users

from esmarket_media.models import Player
from settings import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

helix = twitch.Helix(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
_USER = tp.Union[tp.Union[int, str], tp.List[tp.Union[str, int]]]


def get_users(users: tp.Union[_USER, tp.List[Player]]) -> Users:
    """
    Get user from media API by user's id or display_name

    Usage:
        >>> from esmarket_media.media.twitch_utils import get_users
        >>>
        >>> users = get_users(["Snip3down", "karrigan", 20120002])

    :param users: List of display_names and ids or display_name or user's id
        || List of Player type model object
    :return: User instance
    """
    if any(True for user in users if isinstance(user, Player)):
        users = [user.twitch_name for user in users]

    return helix.users(users)


def get_followers_count(users: tp.Union[_USER, tp.List[Player]]) -> tp.Dict[str, int]:
    """
    Get user's followers from media API by user's id or display_name

    Usage:
        >>> from esmarket_media.media.twitch_utils import get_followers_count
        >>>
        >>> flc = get_followers_count(["Snip3down", "karrigan", 20120002])
        >>> flc
        >>> {"snip3down": 21421, "karrigan": 12421, ...}

    :param users: List of display_names and ids or display_name or user's id
        || List of Player type model object
    :return: Dict with info about followers count
    """
    if any(True for user in users if isinstance(user, Player)):
        users = [user.twitch_name for user in users]

    _users = get_users(users)
    return {user.display_name: user.followers().total for user in _users}
