import random
from aiogram import Router,F
from aiogram.types import Message,CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton
from content.questions import QUESTIONS
from services.games import lottery,quiz_reward

router=Router()

@router.message(F.text=="🎲 Игры")
async def games(message:Message):
    kb=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Лотерея",callback_data="game:lottery")],
        [InlineKeyboardButton(text="🧠 Викторина",callback_data="game:quiz")]
    ])
    await message.answer("🎲 <b>Игры</b>\n\nВыбирай:",reply_markup=kb)

@router.callback_query(F.data=="game:lottery")
async def do_lottery(call:CallbackQuery):
    await call.answer()
    await call.message.answer(await lottery(call.from_user.id))

@router.callback_query(F.data=="game:quiz")
async def make_quiz(call:CallbackQuery):
    await call.answer()
    q=random.choice(QUESTIONS)
    kb=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{i+1}. {opt}",callback_data=f"quiz:{q['answer']}:{i}")]
        for i,opt in enumerate(q["options"])
    ])
    await call.message.answer("🧠 <b>Викторина</b>\n\n"+q["q"],reply_markup=kb)

@router.callback_query(F.data.startswith("quiz:"))
async def answer_quiz(call:CallbackQuery):
    _,answer,index=call.data.split(":")
    ok=int(answer)==int(index)
    await call.answer("Верно!" if ok else "Неверно!")
    await call.message.answer(await quiz_reward(call.from_user.id,ok))
