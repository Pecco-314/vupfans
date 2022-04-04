import datetime
import logging

def quoted(s):
    return "'" + s.replace("'", "''") + "'"

def get_approximate_datetime():
    now = datetime.datetime.now()
    return datetime.datetime(year = now.year, month = now.month, day = now.day, hour = now.hour, minute = now.minute // 30 * 30)

def init_logger():
    logger = logging.getLogger('mylogger')
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        # 使用FileHandler输出到文件
        fh = logging.FileHandler(f'logs/{datetime.datetime.now().timestamp()}.txt')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # 使用StreamHandler输出到屏幕
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        # 添加两个Handler
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger