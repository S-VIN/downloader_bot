import asyncio
import subprocess

import config
from confirmationSettings import ConfirmationTimer
from telethon import TelegramClient, events, types
import logging
import sys
import utils
import schedule
import time

bot = (TelegramClient(
    'vinokurov_archiever_bot',
    config.API_ID,
    config.API_HASH)
       .start(bot_token=config.BOT_TOKEN))
allowed_types = [types.MessageMediaPhoto, types.MessageMediaDocument]

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(config.PATH_FOR_LOGS + 'logs.log')
fileHandler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(fileHandler)
streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(streamHandler)


async def send_confirmation(media_number):
    if media_number > 0:
        await bot.send_message(bot.peer_id, 'Файлы скачаны. Скачано: ' + str(media_number))


# Создаём таймер для отправки подтверждения скачивания
confirmation_timer = ConfirmationTimer(send_confirmation)


@bot.on(events.NewMessage(pattern='/enable_confirmation'))
async def enable_confirmation(event): 
    logger.info('turn on notification')
    confirmation_timer.enable_confirmation()
    await bot.send_message(event.message.peer_id, 'Уведомления о скачивании включены.')


@bot.on(events.NewMessage(pattern='/disable_confirmation'))
async def disable_confirmation(event): 
    logger.info('turn off notification')
    confirmation_timer.disable_confirmation()
    await bot.send_message(event.message.peer_id, 'Уведомления о скачивании выключены.')


@bot.on(events.NewMessage)
async def process_message(event):
    bot.peer_id = event.message.peer_id
    logger.info('process message: ' + str(event.message))
    if await process_media_from_message(event.original_update.message):
        confirmation_timer.increase_media_counter()
        await confirmation_timer.set_timer()


@bot.on(events.MessageDeleted)
async def delete_message(event):
    print('delete message: ', event)
    delete_message_ids = event.deleted_ids
    for id in delete_message_ids:
        file_was_deleted = utils.delete_file_by_id(id)
        if file_was_deleted:
            confirmation_timer.decrease_media_counter()


async def process_media_from_message(tg_message):
    logger.info(tg_message)
    if tg_message.media and allowed_types.count(type(tg_message.media)):

        filename = str(tg_message.date.strftime('%Y-%m-%d')) + '_' + str(tg_message.id)
        filepath = config.PATH_FOR_MEDIA + '/'
        filename_with_path = filepath + filename

        path = await bot.download_media(tg_message.media, filename_with_path)
        logger.debug('file saved to' + path)  # printed after download is done
        return True
    else:
        return False


def copy_files():
    process = subprocess.Popen('cp -r ./ ' + config.PATH_FOR_MEDIA_COPY, cwd=config.PATH_FOR_MEDIA, shell=True)
    print(process.args)
    process.communicate()

    if process.returncode != 0:
        logger.info('copy images, error: ' + str(process.returncode))
    return


async def clock():
    while True:
        schedule.run_pending()
        await asyncio.sleep(100)


schedule.every().day.at("07:00").do(copy_files)
loop = asyncio.get_event_loop()
loop.create_task(clock())
loop.run_forever()
