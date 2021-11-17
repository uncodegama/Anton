import time
import threading

from src.logger import logger


def every(delay: int, task) -> None:
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            logger.exception("Problem while executing repetitive task.")
        next_time += (time.time() - next_time) // delay * delay + delay


def timer_run(timer, func) -> None:
    threading.Thread(target=lambda: every(timer, func)).start()
