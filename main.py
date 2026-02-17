import logging
import json
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
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🌍 Открыть TravelMate",
        web_app=WebAppInfo(url="https://ilshatikv-maker.github.io/my_telegram_bot/web/")
    ))
    
    await message.answer(
        "👋 Добро пожаловать в TravelMate!\n\n"
        "🎯 Здесь ты найдешь:\n"
        "• Информацию о странах\n"
        "• Полезные советы\n"
        "• Погоду и валюты\n\n"
        "👇 Нажми кнопку ниже, чтобы начать:",
        reply_markup=builder.as_markup()
    )

# Обработчик данных из Mini App
@dp.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        value = data.get('value')
        
        if action == 'country':
            responses = {
                'Турция': '🇹🇷 *Турция*\n\n✅ Виза: не нужна до 60 дней\n💵 Валюта: турецкая лира\n🌡️ Погода: +25..+35°C\n\n🏖️ Лучшие курорты: Анталья, Кемер, Алания',
                'Таиланд': '🇹🇭 *Таиланд*\n\n✅ Виза: 30 дней без визы\n💵 Валюта: тайский бат\n🌡️ Погода: +28..+35°C\n\n🏖️ Лучшие курорты: Пхукет, Паттайя, Самуи',
                'Италия': '🇮🇹 *Италия*\n\n✅ Виза: Шенген\n💵 Валюта: евро\n🌡️ Погода: +20..+30°C\n\n🏛️ Лучшие города: Рим, Венеция, Флоренция',
                'Испания': '🇪🇸 *Испания*\n\n✅ Виза: Шенген\n💵 Валюта: евро\n🌡️ Погода: +22..+32°C\n\n🏖️ Лучшие курорты: Барселона, Коста-Брава',
                'ОАЭ': '🇦🇪 *ОАЭ*\n\n✅ Виза: оформляется в аэропорту\n💵 Валюта: дирхам\n🌡️ Погода: +30..+40°C\n\n🏙️ Лучшие города: Дубай, Абу-Даби',
                'Греция': '🇬🇷 *Греция*\n\n✅ Виза: Шенген\n💵 Валюта: евро\n🌡️ Погода: +25..+35°C\n\n🏖️ Лучшие курорты: Крит, Родос, Корфу'
            }
            await message.answer(responses.get(value, 'Информация скоро появится'), parse_mode='Markdown')
            
        elif action == 'tip':
            tips = {
                'visa': '📄 *Виза*\n\n• Шенген оформляй за 2-3 месяца\n• Справка с работы обязательна\n• Страховка нужна для визы',
                'insurance': '🩺 *Страховка*\n\n• Покрытие должно быть от 30 000€\n• Активный отдых оплачивается отдельно',
                'transport': '🚗 *Транспорт*\n\n• Аренда авто от 20€/день\n• Междугородние автобусы дешевле поездов',
                'hotels': '🏨 *Отели*\n\n• Бронируй за 2-3 месяца\n• Обрати внимание на завтраки'
            }
            await message.answer(tips.get(value, 'Совет скоро появится'), parse_mode='Markdown')
            
        elif action == 'weather':
            await message.answer(f"🌤️ Погода в {value}\n\nСкоро здесь будет прогноз погоды!")
            
        elif action == 'currency':
            await message.answer(f"💵 Курс {value}\n\nСкоро здесь будет курс валюты!")
            
    except Exception as e:
        await message.answer("❌ Ошибка обработки данных")
        logging.error(f"Error: {e}")

# Запуск бота
async def main():
    logging.info("Starting TravelMate bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
