import requests
import dao
from util import init_logger

dao = dao.Dao()
logger = init_logger()

def update():
    result_list = []
    for page in range(1, 6):
        logger.info(f"updating room list (page {page})")
        url = f"https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9&page={page}"
        response = requests.get(url).json()
        room_list = response['data']['list']
        for room in room_list:
            result = dao.add_room(room['roomid'], room['uname'], room['face'])
            if result is None:
                result_list.append(room['roomid'])
    return result_list