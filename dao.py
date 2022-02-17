from tkinter import N
import pymysql
import datetime
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

    def search_room(self, keyword):
        sql = f"select * from room where uname like {quoted('%' + keyword + '%')}"
        self.cursor.execute(sql)
        return [{'room_id': room_id, 'uname': uname, 'face': face} for room_id, uname, face in self.cursor.fetchall()]

    def list_medal_names(self, room_id):
        sql = f"select medal_name, count(*) cnt from user where room_id = {room_id} and last_record > '{datetime.datetime.now() - datetime.timedelta(days = 1)}' group by medal_name order by cnt desc;"
        self.cursor.execute(sql)
        return [{'name': name, 'cnt': cnt} for name, cnt in self.cursor.fetchall()]

    def list_medal_levels(self, room_id, level_name):
        sql = f"select medal_level, count(*) from user where room_id = {room_id} and medal_name = {quoted(level_name)} and last_record > '{datetime.datetime.now() - datetime.timedelta(days = 1)}' group by medal_level order by medal_level;"
        self.cursor.execute(sql)
        return [{'level': level, 'cnt': cnt} for level, cnt in self.cursor.fetchall()]
