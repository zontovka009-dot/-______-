from aiogram import Router,F
from aiogram.types import Message
from database.users import get_user
from database.economy import top
from utils.formatting import fmt,title

router=Router()

async def render_profile(user_id):
    u=await get_user(user_id)
    if not u:return "Профиль ещё не создан."
    coins=await top("balance",100000)
    acts=await top("activity",100000)
    cr=next((i+1 for i,x in enumerate(coins) if x["user_id"]==user_id),None)
    ar=next((i+1 for i,x in enumerate(acts) if x["user_id"]==user_id),None)
    name="@"+u["username"] if u["username"] else u["first_name"]
    return (
        "╭━━━━━━━━━━━━━━━━━━╮\n"
        "       👤 <b>ПРОФИЛЬ</b>\n"
        "╰━━━━━━━━━━━━━━━━━━╯\n\n"
        f"Игрок: {name}\n"
        f"💰 TeCoin: <b>{fmt(u['balance'])}</b>\n"
        f"⭐ Activity: <b>{fmt(u['activity'])}</b>\n"
        f"🏅 {title(u['activity'])}\n"
        f"🔥 Серия: <b>{u['streak']} дн.</b>\n"
        f"🏆 TeCoin: #{cr or '—'}\n"
        f"⭐ Activity: #{ar or '—'}\n"
        f"🏆 Лучшая серия: {u['best_streak']} дн."
    )

@router.message(F.text.in_({"👤 Профиль","💰 Баланс","⭐ Актив","🔥 Серия"}))
async def profile_buttons(message:Message):
    await message.answer(await render_profile(message.from_user.id))
