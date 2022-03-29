import datetime

def quoted(s):
    return "'" + s.replace("'", "''") + "'"

def log(s):
    print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {s}")

def get_approximate_datetime():
    now = datetime.datetime.now()
    return datetime.datetime(year = now.year, month = now.month, day = now.day, hour = now.hour, minute = now.minute // 5 * 5)