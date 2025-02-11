import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Bot tokenini va guruh IDlarini bu yerda ko'rsating
BOT_TOKEN = "7884319287:AAFVxSd1iNCUtc-sJpL7XuzfiwXpeWSExKY"
GROUP_IDS = [-1002325563446]  # Guruh IDlarini bu yerga kiriting
SCHEDULE_TIME = "10:00"  # Xabar yuborish vaqti (HH:MM formatida)
ADMIN_ID = 6589557772  # Adminning Telegram ID si

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
scheduler = AsyncIOScheduler()

async def send_scheduled_message():
    message_text = "Salom hammaga! Bu rejalashtirilgan xabar."
    for group_id in GROUP_IDS:
        try:
            await bot.send_message(group_id, message_text)
            logging.info(f"Xabar {group_id} guruhiga yuborildi.")
        except Exception as e:
            logging.error(f"Xatolik yuz berdi: {e}")

async def set_commands():
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="admin_send", description="Admin orqali xabar yuborish")
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Bot ishga tushdi! Guruhlarga har kuni xabar yuboriladi.")

@dp.message_handler(commands=["admin_send"])
async def admin_send_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Yuboriladigan xabar matnini kiriting:")
        @dp.message_handler()
        async def get_admin_message(msg: types.Message):
            for group_id in GROUP_IDS:
                try:
                    await bot.send_message(group_id, msg.text)
                    logging.info(f"Admin xabari {group_id} guruhiga yuborildi.")
                except Exception as e:
                    logging.error(f"Xatolik yuz berdi: {e}")
            await msg.answer("Xabar barcha guruhlarga yuborildi!")
    else:
        await message.answer("Bu buyruq faqat admin uchun!")

async def main():
    await set_commands()
    scheduler.add_job(send_scheduled_message, 'cron', hour=int(SCHEDULE_TIME.split(":" )[0]), minute=int(SCHEDULE_TIME.split(":" )[1]))
    scheduler.start()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
