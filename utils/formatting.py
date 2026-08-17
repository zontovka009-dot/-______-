def fmt(n):
    return f"{int(n):,}".replace(",", " ")

def title(activity):
    if activity<=100:return "🐣 Ньюшка"
    if activity<=300:return "🪑 Усидевшийся"
    if activity<=800:return "⚡ Активчик"
    if activity<=1600:return "🛡️ Ветеран"
    if activity<=2400:return "🧓 Пенсия"
    if activity<=4000:return "🔥 Лютый олд"
    if activity<=6000:return "👑 Легенда чата"
    if activity<=10000:
        stars=min(3,((activity-6001)//2000)+1)
        return "👑 Легенда чата "+"⭐"*stars
    return "🌌 Божество флуда"
