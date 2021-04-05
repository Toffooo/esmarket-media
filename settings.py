from decouple import config

TWITCH_CLIENT_SECRET = config("TWITCH_CLIENT_SECRET", cast=str)
TWITCH_CLIENT_ID = config("TWITCH_CLIENT_ID", cast=str)
TWITCH_APP_NAME = config("TWITCH_APP_NAME", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)
GGSCORE_BASE_LINK = config("GGSCORE_BASE_LINK", cast=str)


class CeleryConfig:
    broker_url = "redis://localhost"
    backend = "redis://localhost"
    RESULT_BACKEND = "redis://localhost"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"
    BEAT_SCHEDULE = {
        "amount-counting": {
            "task": "profile.tasks.amount_counting",
            "schedule": 60.0,
        },
    }


class CeleryConfigDocker:
    broker_url = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
    RESULT_BACKEND = "redis://redis:6379/0"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"
    BEAT_SCHEDULE = {
        "amount-counting": {
            "task": "profile.tasks.amount_counting",
            "schedule": 60.0,
        },
    }
