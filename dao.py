import pymysql
import json

class Dao:
    def __init__(self):
        with open("config.json") as fp:
            config = json.load(fp)
        db_config = config['db']
        self.db = pymysql.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'], db=db_config['db'])
        self.cursor = self.db.cursor()

    def insert(self, room_id, uid, medal_name, medal_level, send_datetime):
        sql = f"insert into user values(null, {room_id}, {uid}, '{medal_name}', {medal_level}, '{send_datetime:%Y-%m-%d %H:%M:%S}')"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            self.db.rollback()
    
    def select_latest(self, room_id, uid):
        sql = f"select max(last_record) from user where room_id={room_id} and uid={uid};"
        self.cursor.execute(sql)
        return self.cursor.fetchone()