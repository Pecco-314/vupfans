import pymysql
import datetime
import json
from util import quoted, get_approximate_datetime, init_logger

logger = init_logger

class Dao:
    def __init__(self):
        with open("config.json") as fp:
            config = json.load(fp)
        self.db_config = config['db']

    def reconnect(self):
        self.connect = pymysql.connect(host=self.db_config['host'], user=self.db_config['user'], password=self.db_config['password'], db=self.db_config['db'])
        self.cursor = self.connect.cursor()

    def is_connected(self):
        try:
            self.connect.ping(reconnect=True)
            return True
        except:
            return False

    def connection(func):
        def wrapper(self, *args, **kw):
            if not self.is_connected():
                self.reconnect()
            return func(self, *args, **kw)
        return wrapper

    def log(func):
        def wrapper(self, *args, **kw):
            try:
                return func(self, *args, **kw)
            except Exception as e:
                logger.error(e)
        return wrapper

    @log
    @connection
    def add_user(self, room_id, uid, medal_id, medal_name, medal_level, send_datetime):
        sql = f"insert into user values(null, {room_id}, {uid}, {medal_id}, {quoted(medal_name)}, {medal_level}, '{send_datetime:%Y-%m-%d %H:%M:%S}')"
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception:
            self.connect.rollback()

    @log
    @connection
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
            self.connect.commit()
        except Exception:
            self.connect.rollback()
        if result is not None:
            return result[0]
        else:
            return None
            
    @log
    @connection     
    def get_rooms(self):
        sql = f"select id from room;"
        self.cursor.execute(sql)
        return [i for (i,) in self.cursor.fetchall()]
            
    @log
    @connection
    def select_latest(self, room_id, uid):
        sql = f"select max(last_record) from user where room_id={room_id} and uid={uid};"
        self.cursor.execute(sql)
        return self.cursor.fetchone()
            
    @log
    @connection
    def search_room(self, keyword):
        sql = f"select * from room where uname like {quoted('%' + keyword + '%')}"
        self.cursor.execute(sql)
        return [{'room_id': room_id, 'uname': uname, 'face': face} for room_id, uname, face in self.cursor.fetchall()]
            
    @log
    @connection
    def list_medal_names(self, room_id):
        sql = f"select medal_id, medal_name, count(*) cnt from user where room_id = {room_id} and last_record > '{get_approximate_datetime() - datetime.timedelta(days = 1)}' group by medal_id, medal_name order by cnt desc;"
        self.cursor.execute(sql)
        return [{'medal': {'id': id, 'name': name}, 'cnt': cnt} for id, name, cnt in self.cursor.fetchall()]
            
    @log
    @connection
    def list_medal_levels(self, room_id, medal_id):
        sql = f"select medal_level, count(*) from user where room_id = {room_id} and medal_id = {quoted(medal_id)} and last_record > '{get_approximate_datetime() - datetime.timedelta(days = 1)}' group by medal_level order by medal_level;"
        self.cursor.execute(sql)
        return [{'level': level, 'cnt': cnt} for level, cnt in 
        self.cursor.fetchall()]
