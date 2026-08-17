from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

def user_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль"),KeyboardButton(text="💰 Баланс")],
            [KeyboardButton(text="⭐ Актив"),KeyboardButton(text="🏆 Рейтинги")],
            [KeyboardButton(text="🔥 Серия"),KeyboardButton(text="🎁 Награда")],
            [KeyboardButton(text="🎲 Игры"),KeyboardButton(text="📦 Ящики")],
            [KeyboardButton(text="🧿 Артефакты"),KeyboardButton(text="🌍 Событие")],
            [KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Пользователи"),KeyboardButton(text="💰 Экономика")],
            [KeyboardButton(text="🌍 События"),KeyboardButton(text="🎟 Промокоды")],
            [KeyboardButton(text="📊 Статистика"),KeyboardButton(text="🛡 Доступ к чатам")],
            [KeyboardButton(text="⚙️ Настройки"),KeyboardButton(text="↩️ Пользовательская панель")]
        ],
        resize_keyboard=True
    )
