import logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5440361816:AAEVkFP2e01j4uYwNJJLBInMmlFpO34uNPY'

bot = Bot(TOKEN)

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
