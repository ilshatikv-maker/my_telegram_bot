import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем клавиатуру главного меню
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Новая поездка"), KeyboardButton(text="📋 Мои поездки")],
            [KeyboardButton(text="🌍 Популярные места"), KeyboardButton(text="⛅ Погода")],
            [KeyboardButton(text="💰 Бюджет"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_name = message.from_user.full_name
    welcome_text = f"""
✈️ Привет, {user_name}!

Я *TravelMate* — твой персональный помощник в путешествиях!

🎯 Что я умею:
• 📍 Помогать планировать поездки
• 🌍 Показывать популярные места
• ⛅ Сообщать погоду в пункте назначения
• 💰 Рассчитывать бюджет путешествия

Выбери действие ниже или используй команды:
/newtrip - Начать новое путешествие
/mytrips - Мои поездки
/weather - Узнать погоду
/help - Помощь
"""
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
📚 *Справочник по командам:*

*/start* - Главное меню
*/newtrip* - Создать новую поездку
*/mytrips* - Показать мои поездки
*/weather <город>* - Погода в городе
*/budget* - Калькулятор бюджета

📞 *Поддержка:*
Если возникли проблемы, напишите: @ваш_аккаунт
"""
    await message.answer(help_text, parse_mode="Markdown")

# Обработка кнопки "Новая поездка"
@dp.message(lambda message: message.text == "📍 Новая поездка")
async def new_trip_handler(message: Message):
    # Создаем inline-клавиатуру для выбора страны
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇹🇷 Турция", callback_data="country_turkey"),
                InlineKeyboardButton(text="🇪🇸 Испания", callback_data="country_spain")
            ],
            [
                InlineKeyboardButton(text="🇹🇭 Таиланд", callback_data="country_thailand"),
                InlineKeyboardButton(text="🇮🇹 Италия", callback_data="country_italy")
            ],
            [
                InlineKeyboardButton(text="🇫🇷 Франция", callback_data="country_france"),
                InlineKeyboardButton(text="🇯🇵 Япония", callback_data="country_japan")
            ],
            [
                InlineKeyboardButton(text="🌍 Другая страна", callback_data="country_other")
            ]
        ]
    )

    trip_text = """
🗺️ *Создание новой поездки*

Выбери страну назначения:

🇹🇷 *Турция* - пляжи, история, восточный колорит
🇪🇸 *Испания* - архитектура, фламенко, средиземноморская кухня
🇹🇭 *Таиланд* - тропики, буддийские храмы, экзотика
🇮🇹 *Италия* - искусство, паста, виноделие
🇫🇷 *Франция* - романтика, мода, гастрономия
🇯🇵 *Япония* - технология, традиции, сакура

*Или напиши город/страну текстом*
Пример: "Бали, Индонезия"
    """

    await message.answer(
        trip_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Обработка кнопки "Мои поездки"
@dp.message(lambda message: message.text == "📋 Мои поездки")
async def my_trips_handler(message: Message):
    trips_text = """
📋 *Ваши поездки:*

1. *Турция 2024* (10-25 августа)
   📍 Анталия
   💰 Бюджет: $1500
   ✅ Активна

2. *Москва выходные* (5-7 июля)
   📍 Москва
   💰 Бюджет: $300
   ✅ Завершена

Используй команду: /mytrips для подробностей
"""
    await message.answer(trips_text, parse_mode="Markdown")

# Обработка кнопки "Популярные места"
@dp.message(lambda message: message.text == "🌍 Популярные места")
async def popular_places_handler(message: Message):
    places_text = """
🌍 *Популярные направления:*

1. *Стамбул, Турция*
   🕌 Айя-София, Голубая мечеть
   🛍️ Гранд-Базар
   💰 Средний бюджет: $800/неделя

2. *Бали, Индонезия*
   🏖️ Пляжи Кута и Семиньяк
   🛕 Храмы Танах Лот
   💰 Средний бюджет: $1000/неделя

3. *Токио, Япония*
   🗼 Tokyo Skytree
   ⛩️ Храм Асакуса
   💰 Средний бюджет: $1500/неделя

Введите город для поиска мест: /places <город>
"""
    await message.answer(places_text, parse_mode="Markdown")

# Обработка кнопки "Погода"
@dp.message(lambda message: message.text == "⛅ Погода")
async def weather_handler(message: Message):
    weather_text = """
⛅ *Проверка погоды*

Я могу показать погоду в любом городе мира!

Просто отправь мне название города, например:
• Москва
• Париж
• Нью-Йорк

Или используй команду: /weather <город>
Пример: /weather Лондон
"""
    await message.answer(weather_text, parse_mode="Markdown")

# Обработка кнопки "Бюджет"
@dp.message(lambda message: message.text == "💰 Бюджет")
async def budget_handler(message: Message):
    budget_text = """
💰 *Калькулятор бюджета*

Рассчитаю примерный бюджет для поездки!

Отправь:
1. Страну назначения
2. Количество дней
3. Количество человек
4. Уровень комфорта (эконом/стандарт/люкс)

Или используй: /budget страна дни люди уровень
Пример: /budget Турция 7 2 стандарт
"""
    await message.answer(budget_text, parse_mode="Markdown")

# Обработка текстовых сообщений (эхо-ответ)
@dp.message()
async def echo_handler(message: Message):
    if message.text.startswith('/'):
        await message.answer("Команда не распознана. Используй /help для списка команд")
    else:
        await message.answer(f"Вы написали: {message.text}\n\nИспользуй кнопки меню или команды!")

# Главная функция
async def main():
    logger.info("Starting TravelMate bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())