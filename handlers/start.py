from aiogram import Router,F
from aiogram.types import Message
from database.users import ensure_user
from keyboards.reply import user_keyboard,admin_keyboard
from utils.permissions import is_admin

router=Router()

@router.message(F.text.in_({"/start","start"}))
async def start(message:Message):
    await ensure_user(message.from_user)
    text=(
        "🌙 Привет! Это <b>The Endy • Genshin</b>.\n\n"
        "Здесь живут TeCoin, Activity, серии, игры, ящики, артефакты и региональные события.\n\n"
        "В группе команды начинаются с <code>.те</code> — например <code>.те профиль</code>."
    )
    await message.answer(
        text,
        reply_markup=admin_keyboard() if is_admin(message.from_user.id) else user_keyboard()
    )
