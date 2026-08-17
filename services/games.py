import random
from database.economy import add_coins,add_activity
from services.loot import random_artifact

async def lottery(user_id):
    roll=random.random()
    if roll<.45:
        c=random.randint(30,100); a=random.randint(5,10)
        await add_coins(user_id,c,"лотерея")
        await add_activity(user_id,a,"лотерея")
        return f"🎉 +{c} TeCoin и +{a} Activity!"
    if roll<.75:
        c=random.randint(100,250)
        await add_coins(user_id,c,"лотерея")
        return f"💰 Ты выиграл {c} TeCoin!"
    if roll<.95:
        _,item=await random_artifact(user_id)
        return f"🧿 Выпал {item[1]} ({item[0]})!"
    c=random.randint(250,600)
    await add_coins(user_id,c,"редкая лотерея")
    return f"✨ Редкий приз: +{c} TeCoin!"

async def quiz_reward(user_id,correct):
    if not correct:
        return "❌ Неверно. Попробуй ещё позже."
    c=random.randint(80,160); a=random.randint(10,25)
    await add_coins(user_id,c,"викторина")
    await add_activity(user_id,a,"викторина")
    return f"🧠 Правильно! +{c} TeCoin и +{a} Activity."
