from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    """Главное меню с кнопками"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Новая поездка"), KeyboardButton(text="📋 Мои поездки")],
            [KeyboardButton(text="🌍 Топ места"), KeyboardButton(text="⛅ Погода")],
            [KeyboardButton(text="💰 Бюджет"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="⭐ Избранное")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_country_keyboard():
    """Клавиатура выбора страны"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇹🇷 Турция", callback_data="country_turkey"),
             InlineKeyboardButton(text="🇹🇭 Таиланд", callback_data="country_thailand")],
            [InlineKeyboardButton(text="🇪🇸 Испания", callback_data="country_spain"),
             InlineKeyboardButton(text="🇮🇹 Италия", callback_data="country_italy")],
            [InlineKeyboardButton(text="🇯🇵 Япония", callback_data="country_japan"),
             InlineKeyboardButton(text="🇺🇸 США", callback_data="country_usa")],
            [InlineKeyboardButton(text="🌍 Другая страна", callback_data="country_other")]
        ]
    )
    return keyboard

def get_trip_actions_keyboard(trip_id):
    """Действия с поездкой"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_trip_{trip_id}"),
             InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_trip_{trip_id}")],
            [InlineKeyboardButton(text="📅 Добавить день", callback_data=f"add_day_{trip_id}"),
             InlineKeyboardButton(text="💰 Изменить бюджет", callback_data=f"edit_budget_{trip_id}")],
            [InlineKeyboardButton(text="📊 Показать детали", callback_data=f"show_details_{trip_id}")]
        ]
    )
    return keyboard