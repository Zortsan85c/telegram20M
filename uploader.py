import os
import asyncio
import aiohttp
from pyrogram import Client

API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
FILE_URL = os.environ.get("FILE_URL")
FILE_NAME = os.environ.get("FILE_NAME")
CHAT_ID = int(os.environ.get("CHAT_ID", 0))
CAPTION = os.environ.get("CAPTION")

async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024 * 1024 * 5)
                    if not chunk:
                        break
                    f.write(chunk)

async def main():
    print(f"Downloading {FILE_NAME} from URL...")
    await download_file(FILE_URL, FILE_NAME)
    print("Download complete. Starting Pyrogram client...")
    
    app = Client("action_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    
    async with app:
        print("Uploading to Telegram via MTProto...")
        await app.send_document(
            chat_id=CHAT_ID,
            document=FILE_NAME,
            caption=CAPTION
        )
        print("Upload success!")
        
    os.remove(FILE_NAME)

if __name__ == "__main__":
    asyncio.run(main())
