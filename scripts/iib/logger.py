
from tool import os
import sys
import is_dev,cwd

# 添加 iib 目录到 Python 路径
iib_dir = os.path.dirname(os.path.abspath(__file__))
if iib_dir not in sys.path:
    sys.path.insert(0, iib_dir)

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(f"{cwd}/log.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
if is_dev:
    logger.addHandler(console_handler)
