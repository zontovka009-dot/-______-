from database.db import connect

async def create_pending(chat_id: int, title: str, requested_by: int):
    db = await connect()
    try:
        cur = await db.execute("SELECT status FROM group_access WHERE chat_id=?", (chat_id,))
        row = await cur.fetchone()
        if row and row["status"] == "approved":
            return False
        await db.execute('''
            INSERT INTO group_access(chat_id,title,status,requested_by)
            VALUES(?,?,?,?)
            ON CONFLICT(chat_id) DO UPDATE SET
                title=excluded.title,
                requested_by=excluded.requested_by,
                status='pending',
                updated_at=CURRENT_TIMESTAMP
        ''', (chat_id,title,"pending",requested_by))
        await db.commit()
        return True
    finally:
        await db.close()

async def set_status(chat_id: int, status: str):
    db = await connect()
    try:
        await db.execute(
            "UPDATE group_access SET status=?,updated_at=CURRENT_TIMESTAMP WHERE chat_id=?",
            (status,chat_id)
        )
        await db.commit()
    finally:
        await db.close()

async def get_status(chat_id: int):
    db = await connect()
    try:
        cur = await db.execute("SELECT * FROM group_access WHERE chat_id=?", (chat_id,))
        return await cur.fetchone()
    finally:
        await db.close()

async def list_groups():
    db = await connect()
    try:
        cur = await db.execute("SELECT * FROM group_access ORDER BY created_at DESC")
        return await cur.fetchall()
    finally:
        await db.close()
