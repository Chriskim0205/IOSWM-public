import asyncio

import telegram

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot_token = TELEGRAM_BOT_TOKEN
chatID = TELEGRAM_CHAT_ID
asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()

bot = telegram.Bot(token=bot_token)

async def send_start_message():
    chat_id = chatID
    await bot.sendMessage(chat_id=chat_id, text="Start Checklist")

async def send_error_message(testwork, issue_link):
    chat_id = chatID
    await bot.sendMessage(chat_id=chat_id, text=f"{testwork} Error Check\n"
                                                f"{issue_link}")

async def send_end_message(min, sec):
    chat_id = chatID
    await bot.sendMessage(chat_id=chat_id, text=f"End Checklist\n"
                                                f"{min}min {sec}sec")
