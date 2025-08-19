import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger("clara")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
