import datetime


today = datetime.datetime.strptime("2018-05-09", "%Y-%m-%d")

print(today.strftime("%b"))
print(today.strftime("%Y"))
print(today.strftime("%d").lstrip("0"))