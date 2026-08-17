import random
from aiogram import Router,F
from aiogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
from database.users import ensure_user,get_user,set_blocked
from database.economy import top,transfer
from database.inventory import list_items
from database.promos import use_promo
from services.games import lottery
from services.events import choose_event,get_event
from utils.formatting import fmt,title
from utils.permissions import is_admin

router=Router()

def parse_command(text):
    parts=text.strip().split()
    if len(parts)<2:return None,[]
    if parts[0].lower()+parts[1].lower()!=".те":return None,[]
    return parts[1].lower(),parts[2:]

@router.message(F.text.regexp(r"^\.те(?:\s|$)"))
async def te(message:Message):
    await ensure_user(message.from_user)
    cmd,args=parse_command(message.text)
    if not cmd:return

    if cmd in {"профиль","баланс","актив","серия"}:
        u=await get_user(message.from_user.id)
        if cmd=="профиль":
            from handlers.profile import render_profile
            await message.answer(await render_profile(message.from_user.id))
        elif cmd=="баланс":
            await message.answer(f"💰 <b>{fmt(u['balance'])} TeCoin</b>")
        elif cmd=="актив":
            await message.answer(f"⭐ <b>{fmt(u['activity'])}</b>\n🏅 {title(u['activity'])}")
        else:
            await message.answer(f"🔥 Серия: <b>{u['streak']} дн.</b>\n🏆 Лучшая: {u['best_streak']} дн.")
        return

    if cmd=="топ":
        field="activity" if args and args[0] in {"актив","activity"} else "balance"
        rows=await top(field,10)
        label="Activity" if field=="activity" else "TeCoin"
        lines=[f"🏆 <b>TOP-10 — {label}</b>",""]
        for i,u in enumerate(rows,1):
            name="@"+u["username"] if u["username"] else u["first_name"]
            value=u["activity"] if field=="activity" else u["balance"]
            lines.append(f"{i}. {name} — {fmt(value)}")
        await message.answer("\n".join(lines))
        return

    if cmd=="лотерея":
        await message.answer(await lottery(message.from_user.id))
        return

    if cmd=="викторина":
        from content.questions import QUESTIONS
        q=random.choice(QUESTIONS)
        kb=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{i+1}. {opt}",
                callback_data=f"quiz:{q['answer']}:{i}"
            )]
            for i,opt in enumerate(q["options"])
        ])
        await message.answer("🧠 <b>Викторина</b>\n\n"+q["q"],reply_markup=kb)
        return

    if cmd=="событие":
        key=choose_event()
        e=get_event(key)
        await message.answer(f"🌍 <b>{e['name']}</b>\n\n{e['desc']}")
        return

    if cmd=="промокод" and args:
        ok,text=await use_promo(args[0],message.from_user.id)
        await message.answer(("🎉 " if ok else "❌ ")+text)
        return

    if cmd=="ящики":
        items=await list_items(message.from_user.id)
        boxes=[x for x in items if x["item_key"].startswith("box_")]
        await message.answer(
            "📦 <b>Ящики</b>\n\n"+
            ("\n".join(f"{x['item_key']} ×{x['quantity']}" for x in boxes) if boxes else "Пока пусто.")
        )
        return

    if cmd=="артефакты":
        items=await list_items(message.from_user.id)
        from content.artifacts import ARTIFACTS
        arts=[]
        for x in items:
            if x["item_key"] in ARTIFACTS:
                data=ARTIFACTS[x["item_key"]]
                arts.append(f"{data[0]} {data[1]} ×{x['quantity']}")
        await message.answer(
            "🧿 <b>Артефакты</b>\n\n" +
            ("\n".join(arts) if arts else "Пока пусто.")
        )
        return

    if cmd=="перевести" and len(args)>=2:
        target=args[0].lstrip("@")
        try:amount=int(args[1])
        except ValueError:
            await message.answer("❌ Сумма должна быть числом.")
            return
        from database.db import connect
        db=await connect()
        try:
            cur=await db.execute("SELECT user_id FROM users WHERE username=?",(target,))
            row=await cur.fetchone()
        finally:
            await db.close()
        if not row:
            await message.answer("❌ Этот пользователь ещё не известен боту.")
            return
        ok,text=await transfer(message.from_user.id,row["user_id"],amount)
        await message.answer(("✅ " if ok else "❌ ")+text)
        return

    if cmd in {"заблокировать","разблокировать"} and is_admin(message.from_user.id) and args:
        target=args[0].lstrip("@")
        from database.db import connect
        db=await connect()
        try:
            cur=await db.execute("SELECT user_id FROM users WHERE username=?",(target,))
            row=await cur.fetchone()
        finally:
            await db.close()
        if not row:
            await message.answer("❌ Пользователь не найден.")
            return
        await set_blocked(row["user_id"],cmd=="заблокировать")
        await message.answer("🔒 Заблокирован." if cmd=="заблокировать" else "🔓 Разблокирован.")
        return

    await message.answer("🌙 Не знаю такую команду. Попробуй <code>.те профиль</code>, <code>.те топ</code> или <code>.те лотерея</code>.")
