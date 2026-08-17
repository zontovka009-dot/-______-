import random
from content.artifacts import ARTIFACTS,RARITY_WEIGHTS
from database.inventory import add_item

async def random_artifact(user_id):
    rarity=random.choices(
        list(RARITY_WEIGHTS),
        weights=list(RARITY_WEIGHTS.values()),
        k=1
    )[0]
    candidates=[k for k,v in ARTIFACTS.items() if v[0]==rarity]
    key=random.choice(candidates)
    await add_item(user_id,key,1)
    return key,ARTIFACTS[key]
