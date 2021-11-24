import logging
import os

from logging.handlers import RotatingFileHandler

from anton.utils.static import LOGGER_FILE_NAME

path = os.path.join(os.getcwd(), LOGGER_FILE_NAME)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
handler = RotatingFileHandler(filename=path, maxBytes=1000000, encoding='UTF-8',
                              backupCount=2)
handler.setFormatter(frmt)

logger = logging.getLogger('anton')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.debug(f"Started Log file in: {path}")
