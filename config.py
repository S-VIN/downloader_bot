PROD_ENV = True

PATH_FOR_MEDIA = './downloads/'
PATH_FOR_MEDIA_COPY = '../download_bot/'

PATH_FOR_LOGS = './logs/'

DEFAULT_CONFIRMATION_PERIOD = 2 * 60 if PROD_ENV else 5

if PROD_ENV:
    print("prod env secrets")
    with open("/run/secrets/downloader_bot_old_school_api_id", "r") as file:
        API_ID = file.read()
    with open("/run/secrets/downloader_bot_old_school_bot_token", "r") as file:
        BOT_TOKEN = file.read()
    with open("/run/secrets/downloader_bot_old_school_api_hash", "r") as file:
        API_HASH = file.read()
else:
    print("dev env secrets")
    import secrets
    API_ID = secrets.API_ID
    BOT_TOKEN = secrets.BOT_TOKEN
    API_HASH = secrets.API_HASH
