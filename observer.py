import datetime
import blivedm.blivedm as blivedm
import dao
from util import log

async def run(room_id):
    log(f"started observing {room_id}")
    client = blivedm.BLiveClient(room_id)
    handler = MyHandler()
    client.add_handler(handler)
    client.start()

    try:
        await client.join()
    finally:
        await client.stop_and_close()

class MyHandler(blivedm.BaseHandler):
    def __init__(self):
        self.dao = dao.Dao()

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        latest = self.dao.select_latest(client.room_id, message.uid)
        send_datetime = datetime.datetime.fromtimestamp(message.timestamp / 1000)
        if latest[0] is None or latest[0] + datetime.timedelta(hours=24) < send_datetime:
            self.dao.add_user(client.room_id, message.uid, message.medal_name, message.medal_level, send_datetime)