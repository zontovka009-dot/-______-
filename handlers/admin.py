from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from config import config
from database.access import list_groups,set_status
from database.promos import list_promos
from keyboards.inline import access_keyboard
from keyboards.reply import admin_keyboard,user_keyboard
from utils.permissions import is_admin

router=Router()

async def require_admin(message):
    return is_admin(message.from_user.id)

@router.message(F.text=="🛡 Доступ к чатам")
async def chat_access(message:Message):
    if not await require_admin(message):return
    groups=await list_groups()
    if not groups:
        await message.answer("🛡 Запросов пока нет.",reply_markup=admin_keyboard())
        return
    text=["🛡 <b>Доступ к чатам</b>",""]
    for g in groups[:30]:
        text.append(f"• {g['title']} — <code>{g['chat_id']}</code> — <b>{g['status']}</b>")
    await message.answer("\n".join(text),reply_markup=admin_keyboard())

@router.callback_query(F.data.startswith("access:"))
async def access_callback(call:CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа.",show_alert=True)
        return
    _,action,chat_id=call.data.split(":")
    status="approved" if action=="approve" else "rejected"
    await set_status(int(chat_id),status)
    await call.answer("Сохранено")
    await call.message.edit_text(call.message.text+f"\n\n<b>Статус: {status}</b>")

@router.message(F.text=="↩️ Пользовательская панель")
async def back_user(message:Message):
    if is_admin(message.from_user.id):
        await message.answer("👤 Пользовательская панель.",reply_markup=user_keyboard())

@router.message(F.text=="👥 Пользователи")
async def users(message:Message):
    if is_admin(message.from_user.id):
        await message.answer(
            "👥 <b>Пользователи</b>\n\n"
            "Поиск: <code>.те найти @username</code>\n"
            "Блокировка: <code>.те заблокировать @username</code>\n"
            "Разблокировка: <code>.те разблокировать @username</code>",
            reply_markup=admin_keyboard()
        )

@router.message(F.text=="🎟 Промокоды")
async def promos(message:Message):
    if not is_admin(message.from_user.id):return
    rows=await list_promos()
    if not rows:
        await message.answer("🎟 Промокодов пока нет.")
        return
    lines=["🎟 <b>Промокоды</b>",""]
    for p in rows[:20]:
        lines.append(f"{p['code']} — {p['reward']} TC — {p['used_count']}/{p['max_uses']}")
    await message.answer("\n".join(lines))

@router.message(F.text=="⚙️ Настройки")
async def settings(message:Message):
    if is_admin(message.from_user.id):
        await message.answer(
            "⚙️ <b>Настройки</b>\n\n"
            "Администраторы задаются через ADMIN_ID_1...ADMIN_ID_5.\n"
            "Доступ к чатам — через раздел «Доступ к чатам».\n"
            "Игровые сообщения из pending/rejected групп игнорируются."
        )
