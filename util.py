import imp


import datetime

def quoted(s):
    return "'" + s.replace("'", "''") + "'"

def log(s):
    print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {s}")