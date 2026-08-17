from database.db import connect

async def add_coins(user_id: int, amount: int, reason: str):
    db = await connect()
    try:
        await db.execute("UPDATE users SET balance=MAX(0,balance+?) WHERE user_id=?", (amount,user_id))
        await db.execute(
            "INSERT INTO transactions(user_id,kind,amount,reason) VALUES(?,?,?,?)",
            (user_id,"coins",amount,reason)
        )
        await db.commit()
    finally:
        await db.close()

async def add_activity(user_id: int, amount: int, reason: str):
    db = await connect()
    try:
        await db.execute(
            "UPDATE users SET activity=MAX(0,activity+?),daily_activity=daily_activity+? WHERE user_id=?",
            (amount,amount,user_id)
        )
        await db.execute(
            "INSERT INTO transactions(user_id,kind,activity,reason) VALUES(?,?,?,?)",
            (user_id,"activity",amount,reason)
        )
        await db.commit()
    finally:
        await db.close()

async def transfer(sender: int, recipient: int, amount: int):
    if amount <= 0 or sender == recipient:
        return False, "Некорректный перевод."

    db = await connect()
    try:
        await db.execute("BEGIN IMMEDIATE")
        cur = await db.execute("SELECT balance,blocked FROM users WHERE user_id=?", (sender,))
        s = await cur.fetchone()
        cur = await db.execute("SELECT user_id,blocked FROM users WHERE user_id=?", (recipient,))
        r = await cur.fetchone()

        if not s or not r:
            await db.rollback()
            return False, "Пользователь не найден."
        if s["blocked"] or r["blocked"]:
            await db.rollback()
            return False, "Один из аккаунтов заблокирован."
        if s["balance"] < amount:
            await db.rollback()
            return False, "Недостаточно TeCoin."

        await db.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (amount,sender))
        await db.execute("UPDATE users SET balance=balance+? WHERE user_id=?", (amount,recipient))
        await db.execute(
            "INSERT INTO transactions(user_id,kind,amount,reason) VALUES(?,?,?,?)",
            (sender,"transfer_out",-amount,f"to:{recipient}")
        )
        await db.execute(
            "INSERT INTO transactions(user_id,kind,amount,reason) VALUES(?,?,?,?)",
            (recipient,"transfer_in",amount,f"from:{sender}")
        )
        await db.commit()
        return True, "Перевод выполнен."
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()

async def top(field: str, limit: int = 10):
    if field not in {"balance","activity","streak"}:
        raise ValueError("Недопустимое поле")
    db = await connect()
    try:
        cur = await db.execute(
            f"SELECT * FROM users WHERE blocked=0 ORDER BY {field} DESC LIMIT ?",
            (limit,)
        )
        return await cur.fetchall()
    finally:
        await db.close()
