from datetime import datetime, timezone
from database.db import connect

async def ensure_user(tg_user):
    db = await connect()
    try:
        await db.execute('''
            INSERT INTO users(user_id,username,first_name)
            VALUES(?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name
        ''', (tg_user.id, tg_user.username, tg_user.first_name))
        await db.commit()
    finally:
        await db.close()

async def get_user(user_id: int):
    db = await connect()
    try:
        cur = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return await cur.fetchone()
    finally:
        await db.close()

async def set_blocked(user_id: int, value: bool):
    db = await connect()
    try:
        await db.execute("UPDATE users SET blocked=? WHERE user_id=?", (int(value), user_id))
        await db.commit()
    finally:
        await db.close()

async def touch_group_activity(tg_user):
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()
    db = await connect()
    try:
        cur = await db.execute("SELECT * FROM users WHERE user_id=?", (tg_user.id,))
        row = await cur.fetchone()
        if not row:
            await db.execute(
                "INSERT INTO users(user_id,username,first_name) VALUES(?,?,?)",
                (tg_user.id, tg_user.username, tg_user.first_name)
            )
            await db.commit()
            cur = await db.execute("SELECT * FROM users WHERE user_id=?", (tg_user.id,))
            row = await cur.fetchone()

        daily_messages = row["daily_messages"] + 1 if row["daily_activity_date"] == today else 1
        daily_activity = row["daily_activity"] if row["daily_activity_date"] == today else 0

        streak = row["streak"]
        if row["last_active_at"]:
            try:
                last_date = datetime.fromisoformat(row["last_active_at"]).date()
                delta = (now.date() - last_date).days
                if delta > 1:
                    streak = 1
                elif delta == 1:
                    streak += 1
            except ValueError:
                streak = max(streak, 1)
        else:
            streak = 1

        await db.execute('''
            UPDATE users SET username=?,first_name=?,last_active_at=?,
            streak=?,best_streak=?,daily_messages=?,
            daily_activity=?,daily_activity_date=?
            WHERE user_id=?
        ''', (
            tg_user.username, tg_user.first_name, now.isoformat(),
            streak, max(row["best_streak"], streak),
            daily_messages, daily_activity, today, tg_user.id
        ))
        await db.commit()
        return daily_messages, streak
    finally:
        await db.close()
