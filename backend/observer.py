import datetime
import blivedm.blivedm as blivedm
from util import init_logger

logger = init_logger()

async def run(room_id, dao):
    client = blivedm.BLiveClient(room_id)
    handler = MyHandler(dao)
    client.add_handler(handler)
    client.start()

    try:
        logger.info(f"started observing room {room_id}")
        await client.join()
    except Exception as e:
        logger.error(f"faild to observe room {room_id}, the message is: {e}")
    finally:
        await client.stop_and_close()

class MyHandler(blivedm.BaseHandler):
    def __init__(self, dao):
        self.dao = dao

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        latest = self.dao.select_latest(client.room_id, message.uid)
        send_datetime = datetime.datetime.fromtimestamp(message.timestamp / 1000)
        if latest[0] is None or latest[0] + datetime.timedelta(hours=24) < send_datetime:
            self.dao.add_user(client.room_id, message.uid, message.medal_room_id, message.medal_name, message.medal_level, send_datetime)