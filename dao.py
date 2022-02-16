import pymysql
import json
from util import quoted

class Dao:
    def __init__(self):
        with open("config.json") as fp:
            config = json.load(fp)
        db_config = config['db']
        self.db = pymysql.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'], db=db_config['db'])
        self.cursor = self.db.cursor()

    def add_user(self, room_id, uid, medal_name, medal_level, send_datetime):
        sql = f"insert into user values(null, {room_id}, {uid}, {quoted(medal_name)}, {medal_level}, '{send_datetime:%Y-%m-%d %H:%M:%S}')"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            self.db.rollback()
    
    def add_room(self, room_id, uname, face):
        sql = f"select id from room where id = {room_id};"
        sql1 = f"insert into room values({room_id}, {quoted(uname)}, {quoted(face)});"
        sql2 = f"update room set uname = {quoted(uname)}, face = {quoted(face)} where id = {room_id};"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result is None:
                self.cursor.execute(sql1)
            else:
                self.cursor.execute(sql2)
            self.db.commit()
        except Exception:
            self.db.rollback()
        if result is not None:
            return result[0]
        else:
            return None
     
    def select_latest(self, room_id, uid):
        sql = f"select max(last_record) from user where room_id={room_id} and uid={uid};"
        self.cursor.execute(sql)
        return self.cursor.fetchone()