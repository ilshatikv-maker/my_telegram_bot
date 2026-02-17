import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Настройки
API_TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    # Создаем кнопку с Mini App
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🌍 Открыть TravelMate Mini App",
        web_app=WebAppInfo(url="https://ilshatikv-maker.github.io/my_telegram_bot/web/")
    ))
    
    await message.answer(
        "👋 Добро пожаловать в TravelMate!\n\n"
        "Нажми кнопку ниже, чтобы открыть мини-приложение:",
        reply_markup=builder.as_markup()
    )

# Обработчик данных из Mini App
@dp.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: types.Message):
    data = message.web_app_data.data
    await message.answer(f"Получены данные: {data}")

# Запуск бота
async def main():
    logging.info("Starting TravelMate bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
