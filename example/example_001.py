# Сделайте так, чтобы число секунд отображалось в виде дни:часы:минуты:секунды.

sec = 123456789

day = 86400
hour = 3600
minute = 60
second = 1

days = sec // day
hours = (sec % day) // hour
minutes = ((sec % day) % hour) // minute
seconds = ((sec % day) % hour) % minute
print(days, hours, minutes, seconds, sep=':')