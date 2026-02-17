from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()


# Команда /newtrip
@router.message(Command("newtrip"))
async def cmd_newtrip(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /newtrip <название поездки>")
        return

    trip_name = " ".join(args[1:])

    # Создаем inline-клавиатуру для выбора действий
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Добавить даты", callback_data=f"add_dates_{trip_name}")],
            [InlineKeyboardButton(text="📍 Добавить место", callback_data=f"add_place_{trip_name}")],
            [InlineKeyboardButton(text="💰 Указать бюджет", callback_data=f"add_budget_{trip_name}")],
            [InlineKeyboardButton(text="✅ Завершить создание", callback_data=f"finish_trip_{trip_name}")]
        ]
    )

    await message.answer(
        f"✈️ *Создаем поездку: {trip_name}*\n\n"
        "Выбери действие:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# Команда /weather
@router.message(Command("weather"))
async def cmd_weather(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /weather <город>")
        return

    city = " ".join(args[1:])

    # Имитация данных погоды (в реальном боте нужно API)
    weather_data = {
        "Москва": {"temp": "+5°C", "desc": "облачно, небольшой снег", "icon": "❄️"},
        "Париж": {"temp": "+12°C", "desc": "переменная облачность", "icon": "⛅"},
        "Лондон": {"temp": "+8°C", "desc": "дождь", "icon": "🌧️"},
        "Токио": {"temp": "+15°C", "desc": "ясно", "icon": "☀️"},
        "Дубай": {"temp": "+28°C", "desc": "солнечно", "icon": "🌞"},
    }

    if city in weather_data:
        data = weather_data[city]
        await message.answer(
            f"{data['icon']} *Погода в {city}*\n\n"
            f"🌡️ Температура: {data['temp']}\n"
            f"📝 Описание: {data['desc']}\n"
            f"🧥 Совет: {'Возьми зонт!' if 'дождь' in data['desc'] else 'Отличная погода для прогулок!'}"
        )
    else:
        await message.answer(f"🌍 Погода для *{city}*\n\n"
                             "☀️ Температура: +20°C\n"
                             "📝 Описание: солнечно, ясно\n"
                             "✨ Идеальная погода для путешествий!", parse_mode="Markdown")


# Команда /budget
@router.message(Command("budget"))
async def cmd_budget(message: Message):
    args = message.text.split()

    if len(args) < 5:
        await message.answer("Использование: /budget <страна> <дни> <люди> <уровень>\n\n"
                             "Уровни: эконом, стандарт, люкс\n"
                             "Пример: /budget Турция 7 2 стандарт")
        return

    country = args[1]
    days = int(args[2])
    people = int(args[3])
    level = args[4].lower()

    # Базовые цены по странам (условные)
    prices = {
        "Турция": {"эконом": 50, "стандарт": 100, "люкс": 200},
        "Таиланд": {"эконом": 40, "стандарт": 80, "люкс": 150},
        "Испания": {"эконом": 70, "стандарт": 120, "люкс": 250},
        "default": {"эконом": 60, "стандарт": 100, "люкс": 200}
    }

    country_prices = prices.get(country, prices["default"])
    daily_price = country_prices.get(level, country_prices["стандарт"])

    total = daily_price * days * people

    breakdown = f"""
💰 *Расчет бюджета для поездки:*

🌍 Страна: {country}
📅 Дней: {days}
👥 Людей: {people}
⭐ Уровень: {level}

📊 *Расчет:*
• {daily_price}$/чел/день × {days} дней × {people} чел
• *Итого: {total}$*

💡 *Рекомендации:*
• Проживание: ~{total * 0.4:.0f}$
• Питание: ~{total * 0.3:.0f}$
• Развлечения: ~{total * 0.2:.0f}$
• Прочее: ~{total * 0.1:.0f}$
"""

    await message.answer(breakdown, parse_mode="Markdown")