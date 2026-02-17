import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os
from dotenv import load_dotenv

load_dotenv()

# Настройки
API_TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Создаем кнопку с Mini App
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="🌍 Открыть TravelMate Mini App",
            web_app=WebAppInfo(url="https://ilshatikv-maker.github.io/my_telegram_bot/web/")
        )
    )
    
    await message.reply(
        "👋 Добро пожаловать в TravelMate!\n\n"
        "Нажми кнопку ниже, чтобы открыть мини-приложение:",
        reply_markup=keyboard
    )

# Обработчик данных из Mini App
@dp.message_handler(content_types=['web_app_data'])
async def handle_web_app_data(message: types.Message):
    data = message.web_app_data.data
    await message.answer(f"Получены данные: {data}")

# Запуск бота
if __name__ == '__main__':
    logging.info("Starting TravelMate bot...")
    executor.start_polling(dp, skip_updates=True)
