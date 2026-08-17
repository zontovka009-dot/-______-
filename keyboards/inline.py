from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

def access_keyboard(chat_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Разрешить чат",callback_data=f"access:approve:{chat_id}")],
        [InlineKeyboardButton(text="❌ Отклонить",callback_data=f"access:reject:{chat_id}")]
    ])

def top_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 TeCoin",callback_data="top:coins"),
         InlineKeyboardButton(text="⭐ Activity",callback_data="top:activity")]
    ])
