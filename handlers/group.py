from aiogram import Router,F
from aiogram.types import Message,ChatMemberUpdated
from database.access import create_pending,get_status
from services.activity import process_message
from config import config
from keyboards.inline import access_keyboard

router=Router()

@router.my_chat_member()
async def added_to_chat(event:ChatMemberUpdated):
    new=event.new_chat_member.status
    old=event.old_chat_member.status
    if new in {"member","administrator"} and old in {"left","kicked"}:
        chat_id=event.chat.id
        title=event.chat.title or "Без названия"
        created=await create_pending(chat_id,title,event.from_user.id)
        if not created:return

        for admin_id in config.admin_ids:
            try:
                await event.bot.send_message(
                    admin_id,
                    "🛡 <b>Новый запрос на подключение The Endy</b>\n\n"
                    f"Чат: <b>{title}</b>\n"
                    f"ID: <code>{chat_id}</code>\n\n"
                    "До решения бот не обрабатывает игровые сообщения.",
                    reply_markup=access_keyboard(chat_id)
                )
            except Exception:
                pass

@router.message(F.chat.type.in_({"group","supergroup"}))
async def track_group(message:Message):
    access=await get_status(message.chat.id)
    if not access or access["status"]!="approved":
        return
    await process_message(message.from_user)
