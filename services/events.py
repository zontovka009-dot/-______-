import random
from content.regions import MAIN_WEIGHTS,SPECIAL_WEIGHTS,MOON_WEIGHTS,REGIONS

def weighted(weights):
    return random.choices(list(weights),weights=list(weights.values()),k=1)[0]

def choose_event():
    if random.random()<.8:
        return weighted(MAIN_WEIGHTS)
    special=weighted(SPECIAL_WEIGHTS)
    if special=="nod":
        return weighted(MOON_WEIGHTS)
    return special

def get_event(key):
    return REGIONS[key]
