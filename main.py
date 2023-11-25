import settings
from telethon import TelegramClient, events, types
from peer import Peer
import logging
import sys

bot = TelegramClient('vinokurov_archiever_bot', settings.API_ID, settings.API_HASH).start(bot_token=settings.BOT_TOKEN)
allowed_types = [types.MessageMediaPhoto, types.MessageMediaDocument]

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(settings.PATH_FOR_LOGS + 'logs.log')
fileHandler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(fileHandler)
streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(streamHandler)


@bot.on(events.NewMessage)
async def process_message(event):
    await process_media_from_message(event.original_update.message)


async def process_media_from_message(tg_message):
    logger.info(tg_message)
    if tg_message.media and allowed_types.count(type(tg_message.media)):

        filename = str(tg_message.date.strftime('%Y-%m-%d')) + '_' + str(tg_message.id)
        filepath = settings.PATH_FOR_MEDIA + str(Peer.from_tg_peer(tg_message.peer_id).id) + '/'
        filename_with_path = filepath + filename

        path = await bot.download_media(tg_message.media, filename_with_path)
        logger.debug('file saved to' + path)  # printed after download is done


bot.run_until_disconnected()
