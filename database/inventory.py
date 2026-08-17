from database.db import connect

async def add_item(user_id:int,item_key:str,qty:int=1):
    db=await connect()
    try:
        await db.execute('''
            INSERT INTO inventory(user_id,item_key,quantity) VALUES(?,?,?)
            ON CONFLICT(user_id,item_key)
            DO UPDATE SET quantity=quantity+excluded.quantity
        ''',(user_id,item_key,qty))
        await db.commit()
    finally:
        await db.close()

async def list_items(user_id:int):
    db=await connect()
    try:
        cur=await db.execute(
            "SELECT * FROM inventory WHERE user_id=? AND quantity>0 ORDER BY item_key",
            (user_id,)
        )
        return await cur.fetchall()
    finally:
        await db.close()
