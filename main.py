import asyncio
from threading import Thread
import spider
import observer
from util import log
 
async def production_task():
    while True:
        room_list = spider.update()
        log(f"updated room list")
        for room in room_list:
            asyncio.run_coroutine_threadsafe(observer.run(room),
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