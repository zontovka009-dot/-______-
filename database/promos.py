from datetime import datetime, timezone
from database.db import connect

async def create_promo(code,reward,max_uses,expires_at,created_by):
    db=await connect()
    try:
        await db.execute(
            "INSERT INTO promo_codes(code,reward,max_uses,expires_at,created_by) VALUES(?,?,?,?,?)",
            (code.upper(),reward,max_uses,expires_at,created_by)
        )
        await db.commit()
    finally:
        await db.close()

async def use_promo(code,user_id):
    code=code.upper()
    db=await connect()
    try:
        await db.execute("BEGIN IMMEDIATE")
        cur=await db.execute("SELECT * FROM promo_codes WHERE code=?",(code,))
        p=await cur.fetchone()
        if not p:
            await db.rollback()
            return False,"Промокод не найден."
        if p["expires_at"]:
            try:
                if datetime.fromisoformat(p["expires_at"]) <= datetime.now(timezone.utc):
                    await db.rollback()
                    return False,"Промокод истёк."
            except ValueError:
                pass
        if p["used_count"] >= p["max_uses"]:
            await db.rollback()
            return False,"Лимит использований исчерпан."

        cur=await db.execute(
            "SELECT 1 FROM promo_uses WHERE code=? AND user_id=?",(code,user_id)
        )
        if await cur.fetchone():
            await db.rollback()
            return False,"Ты уже использовал этот промокод."

        await db.execute("INSERT INTO promo_uses(code,user_id) VALUES(?,?)",(code,user_id))
        await db.execute(
            "UPDATE promo_codes SET used_count=used_count+1 WHERE code=?",(code,)
        )
        await db.execute(
            "UPDATE users SET balance=balance+? WHERE user_id=?",(p["reward"],user_id)
        )
        await db.execute(
            "INSERT INTO transactions(user_id,kind,amount,reason) VALUES(?,?,?,?)",
            (user_id,"promo",p["reward"],f"promo:{code}")
        )
        await db.commit()
        return True,f"+{p['reward']} TeCoin"
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()

async def list_promos():
    db=await connect()
    try:
        cur=await db.execute("SELECT * FROM promo_codes ORDER BY created_at DESC")
        return await cur.fetchall()
    finally:
        await db.close()
