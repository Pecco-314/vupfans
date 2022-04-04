import asyncio
from threading import Thread
import spider
import observer
from util import init_logger
from dao import Dao
import aiohttp

dao = Dao()
logger = init_logger()

async def production_task():
    old_rooms = dao.get_rooms()
    for room in old_rooms:
        asyncio.run_coroutine_threadsafe(observer.run(room, dao), thread_loop)
    while True:
        new_rooms = spider.update()
        logger.info(f"updated room list")
        for room in new_rooms:
            asyncio.run_coroutine_threadsafe(observer.run(room, dao),
                        thread_loop)
        await asyncio.sleep(900)
 
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
 
thread_loop = asyncio.new_event_loop()
run_loop_thread = Thread(target=start_loop, args=(thread_loop,))
run_loop_thread.start()
 
advocate_loop = asyncio.get_event_loop()
advocate_loop.run_until_complete(production_task())