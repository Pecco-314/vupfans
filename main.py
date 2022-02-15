import json
import datetime
import asyncio
import blivedm.blivedm as blivedm
import dao

with open("config.json") as fp:
    config = json.load(fp)
room_ids = config['list']

async def run():
    clients = [blivedm.BLiveClient(room_id) for room_id in room_ids]
    handler = MyHandler()
    for client in clients:
        client.add_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))

async def main():
    await run()

class MyHandler(blivedm.BaseHandler):
    def __init__(self):
        self.dao = dao.Dao()

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        latest = self.dao.select_latest(client.room_id, message.uid)
        send_datetime = datetime.datetime.fromtimestamp(message.timestamp / 1000)
        if latest[0] is None or latest[0] + datetime.timedelta(hours=24) < send_datetime:
            self.dao.insert(client.room_id, message.uid, message.medal_name, message.medal_level, send_datetime)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())