PROD_ENV = False

PATH_FOR_MEDIA = './media_from_dialogs/'
PATH_FOR_LOGS = './logs/'

DEFAULT_CONFIRMATION_PERIOD = 2 * 60 if PROD_ENV else 5

if PROD_ENV:
    with open("/run/secrets/downloader_bot_old_school_api_id", "r") as file:
        API_ID = file.read()
    with open("/run/secrets/downloader_bot_old_school_bot_token", "r") as file:
        BOT_TOKEN = file.read()
    with open("/run/secrets/downloader_bot_old_school_api_hash", "r") as file:
        API_HASH = file.read()
else:
    import secrets
    API_ID = secrets.API_ID
    BOT_TOKEN = secrets.BOT_TOKEN
    API_HASH = secrets.API_HASH
