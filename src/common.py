import time
import traceback
import threading


def every(delay: int, task) -> None:
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
        next_time += (time.time() - next_time) // delay * delay + delay


def timer_run(timer, func) -> None:
    threading.Thread(target=lambda: every(timer, func)).start()
