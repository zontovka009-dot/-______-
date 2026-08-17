from database.users import touch_group_activity
from database.economy import add_activity

async def process_message(user):
    daily_messages, streak = await touch_group_activity(user)
    # Только 7 ступеней пассивной награды в день.
    if daily_messages in {1,3,5,8,12,16,20}:
        await add_activity(user.id,2,"пассивная активность")
    return daily_messages, streak
