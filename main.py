from pyrogram import Client
from pyrogram import filters
import settings

app = Client("vinokurov_archiever_bot", api_id=settings.API_ID, api_hash=settings.API_HASH, bot_token=settings.BOT_TOKEN)

last_id = 0

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")
    if current / total == 1:
        await app.send_message(chat_id=last_id, text="Скачал.")

@app.on_message(filters.media)
async def echo(client, message):
    print('Downloading started, last.id=', message.chat.id)
    global last_id
    last_id = message.chat.id
    file = await app.download_media(message, progress=progress)
    print('Downloading ended')


app.run()

