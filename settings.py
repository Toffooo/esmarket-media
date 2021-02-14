from decouple import config


TWITCH_CLIENT_SECRET = config("TWITCH_CLIENT_SECRET", cast=str)
TWITCH_CLIENT_ID = config("TWITCH_CLIENT_ID", cast=str)
TWITCH_APP_NAME = config("TWITCH_APP_NAME", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)
