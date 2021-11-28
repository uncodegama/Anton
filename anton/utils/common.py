import threading
import time

from pydantic.typing import Callable

from anton.utils.logger import logger


def every(delay: int, task: Callable) -> None:
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            logger.exception("Problem while executing repetitive task.")
        next_time += (time.time() - next_time) // delay * delay + delay


def timer_run(timer: int, func: Callable) -> None:
    threading.Thread(target=lambda: every(timer, func)).start()
